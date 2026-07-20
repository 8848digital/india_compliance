# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import calendar
import json
import os
from collections import defaultdict

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.query_builder.functions import IfNull
from frappe.utils import cint, cstr, flt, get_first_day, get_last_day
from openpyxl.cell.cell import MergedCell

from india_compliance.gst_india.constants import (
    INVOICE_DOCTYPES,
    STATE_NUMBERS,
    TAXABLE_GST_TREATMENTS,
)
from india_compliance.gst_india.overrides.transaction import is_inter_state_supply
<<<<<<< HEAD
from india_compliance.gst_india.report.gstr_1.gstr_1 import GSTR11A11BData
from india_compliance.gst_india.report.gstr_3b_details.gstr_3b_details import (
    IneligibleITC,
)
=======
>>>>>>> 26dbbe72 (refactor: gstr_3b_report)
from india_compliance.gst_india.utils import (
    get_data_file_path,
    get_gst_accounts_by_type,
    get_period,
)
from india_compliance.gst_india.utils.exporter import ExcelExporter
<<<<<<< HEAD
=======
from india_compliance.gst_india.utils.gstr3b.gstr3b_data import GSTR3BInvoices
from india_compliance.gst_india.utils.gstr_1.gstr_1_data import (
    GSTR1Invoices,
    GSTR11A11BData,
)
>>>>>>> 26dbbe72 (refactor: gstr_3b_report)
from india_compliance.gst_india.utils.itc_claim import (
    apply_period_filter as _apply_itc_period_filter,
)

VALUES_TO_UPDATE = ["iamt", "camt", "samt", "csamt"]

# Map GST treatment on SI items to the corresponding 3.1 section key
GST_TREATMENT_SECTION_MAP = {
    "Nil-Rated": "osup_nil_exmp",
    "Exempted": "osup_nil_exmp",
    "Zero-Rated": "osup_zero",
    "Non-GST": "osup_nongst",
    "Taxable": "osup_det",
}

# GST categories that need to be reported in section 3.2 (inter-state supplies)
INTER_STATE_GST_CATEGORIES = frozenset(
    {"Unregistered", "Registered Composition", "UIN Holders"}
)

# Maps GSTR-3B sub-category labels to the 'ty' key in the JSON template (ITC Available)
ITC_AVAILABLE_SUB_CATEGORY_MAP = {
    "Import Of Goods": "IMPG",
    "Import Of Service": "IMPS",
    "ITC on Reverse Charge": "ISRC",
    "Input Service Distributor": "ISD",
    "All Other ITC": "OTH",
}

# Maps GSTR-3B sub-category labels to the index in itc_rev list (ITC Reversed)
ITC_REVERSED_INDEX_MAP = {
    "As per rules 42 & 43 of CGST Rules and section 17(5)": 0,  # ty = "RUL"
    "Others": 1,
}

# Maps invoice amount fields to JSON key names used in the ITC section
_ITC_FIELD_MAP = {
    "iamt": "igst_amount",
    "camt": "cgst_amount",
    "samt": "sgst_amount",
    "csamt": "cess_amount",
}
from typing import ClassVar


class GSTR3BReport(Document):
    @property
    def filing_status(self):
        status = "Not Filed"
        if not (self.company_gstin and self.month_or_quarter and self.year):
            return status

        period = get_period(self.month_or_quarter, self.year)
        filters = {
            "gstin": self.company_gstin,
            "return_period": period,
            "return_type": "GSTR3B",
        }
        status = frappe.db.get_value("GST Return Log", filters, "filing_status")

        return status or "Not Filed"

    def validate(self):
        self.json_output = ""
        if not self.company_gstin:
            frappe.throw(_("Please enter GSTIN for Company {0}").format(self.company))

        if self.is_new():
            existing_report = frappe.db.get_value(
                "GSTR 3B Report",
                {
                    "company_gstin": self.company_gstin,
                    "month_or_quarter": self.month_or_quarter,
                    "year": self.year,
                },
                "name",
            )

            if existing_report:
                frappe.throw(
                    _("GSTR-3B Report for {0} {1} already exists: {2}").format(
                        self.month_or_quarter,
                        self.year,
                        frappe.utils.get_link_to_form("GSTR 3B Report", existing_report),
                    ),
                    title=_("Report Already Exists"),
                )

        self.generation_status = "In Process"

        if self.enqueue_report:
            return

        self.get_data()

    def on_update(self):
        if not self.enqueue_report:
            return

        frappe.msgprint(_("Initiated report generation in background"), alert=True)
        frappe.enqueue_doc(
            "GSTR 3B Report",
            self.name,
            "get_data",
            queue="long",
            enqueue_after_commit=True,
        )

    def get_data(self):
        try:
            self.report_dict = json.loads(get_json("gstr_3b_report_template"))

            if not self.company_gstin:
                frappe.throw(
                    _("Please enter GSTIN for Company {0}").format(self.company)
                )
            self.report_dict["gstin"] = self.company_gstin
            self.report_dict["ret_period"] = get_period(
                self.month_or_quarter, self.year
            )
            self.month_or_quarter_no = get_period(self.month_or_quarter)
            self.from_date = get_first_day(
                f"{cint(self.year)}-{self.month_or_quarter_no[0]}-01"
            )
            self.to_date = get_last_day(
                f"{cint(self.year)}-{self.month_or_quarter_no[1]}-01"
            )

            gstr1_filters = self._get_gstr1_filters()
            gstr3b_filters = self._get_gstr3b_filters()

            # Tables 3.1 (outward), 3.1.1 (eco), 3.2 (inter-state)
            # Source: GSTR1Invoices (Sales Invoice data)
            self.process_outward_supplies(gstr1_filters)

            # Table 3.1(d) — Inward supplies liable to reverse charge
            # Source: GSTR3BInvoices (Purchase Invoice, RC only)
            self.process_reverse_charge_inward(gstr3b_filters)

            # Table 3.3 — Advances received / adjusted
            # Source: GSTR11A11BData (already from gstr_1_data.py)
            self.set_advances_received_or_adjusted()

            # Table 4 — ITC eligible / reversed / net / ineligible
            # Source: GSTR3BInvoices (Purchase Invoice, Bill of Entry, Journal Entry)
            self.process_itc(gstr3b_filters)

            # Table 5 — Inward nil / exempt / non-GST supplies
            # Source: GSTR3BInvoices (Purchase Invoice)
            self.process_inward_nil_exempt(gstr3b_filters)

            self.missing_field_invoices = self.get_missing_field_invoices()
            self.report_dict = format_values(self.report_dict)
            self.json_output = frappe.as_json(self.report_dict)
            self.generation_status = "Generated"

            if self.enqueue_report:
                self.db_set(
                    {
                        "json_output": self.json_output,
                        "missing_field_invoices": self.missing_field_invoices,
                        "generation_status": self.generation_status,
                    }
                )

        except Exception as e:
            self.generation_status = "Failed"
            self.db_set({"generation_status": self.generation_status})
            frappe.db.commit()  # nosemgrep
            raise e

        finally:
            # after_commit so the client never reloads before the row is visible
            frappe.publish_realtime(
                "gstr3b_report_generation",
                doctype=self.doctype,
                docname=self.name,
                after_commit=True,
            )

    def _get_gstr1_filters(self):
        """Filters for GSTR1Invoices (Sales Invoice data)."""
        return frappe._dict(
            {
                "company": self.company,
                "company_gstin": self.company_gstin,
                "from_date": self.from_date,
                "to_date": self.to_date,
            }
        )

    def _get_gstr3b_filters(self):
        """Filters for GSTR3BInvoices (Purchase / BOE / JE data)."""
        return frappe._dict(
            {
                "company": self.company,
                "company_gstin": self.company_gstin,
                "from_date": self.from_date,
                "to_date": self.to_date,
                "filter_by": self.filter_by,
            }
        )

    def apply_itc_period_filter(self, query, doc):
        return _apply_itc_period_filter(
            query,
            doc,
            self.from_date,
            self.to_date,
            filter_by=self.filter_by,
        )

    def process_outward_supplies(self, gstr1_filters):
        """
        Populate sections 3.1 (outward supply details), 3.1.1 (e-commerce RC
        supplies) and 3.2 (inter-state supplies) from Sales Invoice line-item
        data provided by GSTR1Invoices.

        Mapping:
          gst_treatment == "Nil-Rated" / "Exempted"  → osup_nil_exmp  (txval only)
          gst_treatment == "Non-GST"                  → osup_nongst    (txval only)
          gst_treatment == "Zero-Rated"               → osup_zero      (txval + iamt + csamt)
          gst_treatment == "Taxable" (non-RC)         → osup_det       (txval + all taxes)
          gst_treatment == "Taxable" (RC)             → osup_det       (txval only, no taxes)
          gst_treatment == "Taxable" (RC + eco GSTIN) → eco_reg_sup   (txval only, deducted from osup_det)
        """
        gstr1 = GSTR1Invoices(gstr1_filters)
        invoices = gstr1.get_invoices_for_item_wise_summary()

        inter_state_supply = {}
        eco_taxable_value = 0.0

        for invoice in invoices:
            gst_treatment = invoice.gst_treatment
            section_key = GST_TREATMENT_SECTION_MAP.get(gst_treatment)
            if not section_key:
                continue

            taxable_value = invoice.taxable_value or 0
            section = self.report_dict["sup_details"][section_key]
            section["txval"] += taxable_value

            if gst_treatment == "Taxable":
                if not invoice.is_reverse_charge:
                    section["iamt"] += invoice.igst_amount or 0
                    section["camt"] += invoice.cgst_amount or 0
                    section["samt"] += invoice.sgst_amount or 0
                    section["csamt"] += invoice.total_cess_amount or 0

                if invoice.is_reverse_charge and invoice.ecommerce_gstin:
                    eco_taxable_value += taxable_value

                self._update_inter_state_supply(
                    invoice, taxable_value, inter_state_supply
                )

            elif gst_treatment == "Zero-Rated":
                section["iamt"] += invoice.igst_amount or 0
                section["csamt"] += invoice.total_cess_amount or 0

        self.report_dict["eco_dtls"]["eco_reg_sup"]["txval"] = eco_taxable_value
        self.report_dict["sup_details"]["osup_det"]["txval"] -= eco_taxable_value

        self.set_inter_state_supply(inter_state_supply)

    def _update_inter_state_supply(self, invoice, taxable_value, inter_state_supply):
        """
        Collect inter-state supply data for section 3.2.
        Only Unregistered, Registered Composition and UIN Holder categories qualify.
        """
        gst_category = invoice.gst_category
        if gst_category not in INTER_STATE_GST_CATEGORIES:
            return

        place_of_supply = invoice.place_of_supply or "00-Other Territory"
        doc = frappe._dict(
            {
                "gst_category": gst_category,
                "place_of_supply": place_of_supply,
                "company_gstin": invoice.company_gstin,
            }
        )

        if not is_inter_state_supply(doc):
            return

        key = (gst_category, place_of_supply)
        inter_state_supply.setdefault(
            key,
            {
                "txval": 0.0,
                "pos": place_of_supply.split("-")[0],
                "iamt": 0.0,
            },
        )
        inter_state_supply[key]["txval"] += taxable_value
        inter_state_supply[key]["iamt"] += invoice.igst_amount or 0

<<<<<<< HEAD
    def set_inter_state_supply(self, inter_state_supply):
        inter_state_supply_map = {
            "Unregistered": "unreg_details",
            "Registered Composition": "comp_details",
            "UIN Holders": "uin_details",
=======
        inter_state_supply[key]["txval"] += invoice.taxable_value or 0
        inter_state_supply[key]["iamt"] += igst_amount

    def _process_inward_itc(self):
        """
        Tables 4 (ITC) and 5 (nil/exempt inward)
        """
        inward_invoices = GSTR3BInwardInvoices(self._get_filters())
        inward_data = inward_invoices.get_all_data(group_by_invoice=True)

        self.update_inward_json(inward_data)

    def update_inward_json(self, data):
        itc_elg = self.report_dict["itc_elg"]
        itc_index = {
            section: {row["ty"]: row for row in rows}
            for section, rows in itc_elg.items()
            if isinstance(rows, list)
        }
        inward_sup_index = {row["ty"]: row for row in self.report_dict["inward_sup"]["isup_details"]}

        for invoice in data:
            if invoice.get("invoice_category") in INWARD_NIL_EXEMPT_SECTION_MAP:
                self._update_inward_nil_exempt_section(invoice, inward_sup_index)
            else:
                self._update_eligible_itc_section(invoice, itc_index, itc_elg["itc_net"])

    def _update_eligible_itc_section(self, invoice, itc_index, net_itc):
        section_data = INWARD_ITC_SECTION_MAP.get(invoice.get("invoice_sub_category"))
        if not section_data:
            return

        section_key, ty, net_sign = section_data
        entry = itc_index.get(section_key, {}).get(ty)
        if not entry:
            return

        for json_key, field in ITC_AMOUNT_KEYS.items():
            amount = invoice.get(field) or 0
            entry[json_key] += amount
            net_itc[json_key] += amount * net_sign

    def _update_inward_nil_exempt_section(self, invoice, inward_sup_index):
        ty = INWARD_NIL_EXEMPT_SECTION_MAP.get(invoice.get("invoice_sub_category"))
        if not ty:
            return

        entry = inward_sup_index.get(ty)
        if not entry:
            return

        entry["inter"] += invoice.get("inter") or 0
        entry["intra"] += invoice.get("intra") or 0


def get_json(template):
    file_path = os.path.join(os.path.dirname(__file__), f"{template}.json")
    with open(file_path) as f:  # nosemgrep
        return cstr(f.read())


def format_values(data, precision=2):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (int, float)):
                data[key] = flt(value, precision)
            elif isinstance(value, dict) or isinstance(value, list):
                format_values(value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, (int, float)):
                data[i] = flt(item, precision)
            elif isinstance(item, dict) or isinstance(item, list):
                format_values(item)

    return data


def get_file_name(name):
    report = frappe.db.get_value(
        "GSTR 3B Report",
        name,
        ["company_gstin", "month_or_quarter", "year"],
        as_dict=True,
    )
    return f"GSTR-3B-{report.company_gstin}-{report.month_or_quarter.replace(' ', '')}-{report.year}"


@frappe.whitelist()
def make_json(name: str):
    frappe.has_permission("GSTR 3B Report", throw=True)

    json_data = frappe.get_value("GSTR 3B Report", name, "json_output")
    frappe.local.response.filename = f"{get_file_name(name)}.json"
    frappe.local.response.filecontent = json_data
    frappe.local.response.type = "download"


@frappe.whitelist()
def download_gstr3b_as_excel(name: str):
    """Download GSTR 3B report as Excel file"""
    frappe.has_permission("GSTR 3B Report", throw=True)
    json_data = frappe.get_value("GSTR 3B Report", name, "json_output")

    if not json_data:
        frappe.throw(_("Report data not found. Please generate the report."))

    data = json.loads(json_data)
    exporter = GSTR3BExcelExporter(data)
    exporter.generate_excel(get_file_name(name))


@frappe.whitelist()
def download_gstr3b_as_pdf(name: str):
    """Download GSTR 3B report as PDF file"""
    frappe.has_permission("GSTR 3B Report", throw=True)

    frappe.local.response.filename = f"{get_file_name(name)}.pdf"
    frappe.local.response.filecontent = frappe.get_print(
        "GSTR 3B Report", name, print_format="GSTR-3B", as_pdf=True, no_letterhead=True
    )
    frappe.local.response.type = "pdf"


class GSTR3BExcelExporter:
    """
    Export GSTR-3B data to Excel format using the official template.

    This class handles data transformation and mapping from JSON to Excel cells
    following the official GSTR-3B offline utility format.
    """

    TEMPLATE_FILE = get_data_file_path("gstr3b_excel_utility_v5.7.xlsx")
    WORKSHEET_NAME = "GSTR-3B"

    _STATE_CODE_TO_NAME: ClassVar[dict] = {code: state for state, code in STATE_NUMBERS.items()}

    # Row mappings for each section (consistent with JSON keys)
    ROWS: ClassVar[dict] = {
        # Header info
        "gstin": 5,
        "year": 5,
        "month": 6,
        # Section 3.1 - Outward supplies
        "osup_det": 11,
        "osup_zero": 12,
        "osup_nil_exmp": 13,
        "isup_rev": 14,
        "osup_nongst": 15,
        "eco_reg_sup": 23,
        # Section 3.2 - Inter-state
        "inter_state_start": 88,
        # Section 4 - ITC
        "itc_import_goods": 31,
        "itc_import_services": 32,
        "itc_reverse_charge": 33,
        "itc_isd": 34,
        "itc_others": 35,
        "itc_reversed_rules": 37,
        "itc_reversed_others": 38,
        "itc_reclaimed": 41,
        "itc_ineligible": 42,
        # Section 5 - Inward supplies
        "inward_gst": 48,
        "inward_non_gst": 49,
    }

    HEADER_COLUMNS: ClassVar[dict] = {
        "gstin": 3,
        "year": 7,
        "month": 7,
    }

    # Section 3.1 - Tax columns
    TAX_COLUMNS: ClassVar[dict] = {
        "txval": 3,
        "iamt": 4,
        "camt": 5,
        "samt": 6,
        "csamt": 7,
    }

    # Section 4 - ITC columns
    ITC_COLUMNS: ClassVar[dict] = {
        "iamt": 3,
        "camt": 4,
        "samt": 5,
        "csamt": 6,
    }

    # Section 5 - Inward supplies columns
    INWARD_COLUMNS: ClassVar[dict] = {
        "inter": 4,
        "intra": 5,
    }

    # ITC type mappings based on 'ty' field in JSON
    ITC_AVAILABLE_TYPES: ClassVar[dict] = {
        "IMPG": "itc_import_goods",
        "IMPS": "itc_import_services",
        "ISRC": "itc_reverse_charge",
        "ISD": "itc_isd",
        "OTH": "itc_others",
    }

    ITC_REVERSED_TYPES: ClassVar[dict] = {
        "RUL": "itc_reversed_rules",
        "OTH": "itc_reversed_others",
    }

    INWARD_SUPPLY_TYPES: ClassVar[dict] = {
        "GST": "inward_gst",
        "NONGST": "inward_non_gst",
    }

    COLUMN_SETS = {
        "tax": ["txval", "iamt", "camt", "samt", "csamt"],
        "itc": ["iamt", "camt", "samt", "csamt"],
        "import_itc": ["iamt", "csamt"],
        "inward": ["inter", "intra"],
        "zero_rated": ["txval", "iamt", "csamt"],
        "taxable_only": ["txval"],
    }

    def __init__(self, data):
        self.data = data
        self.gstin = data.get("gstin")
        self.worksheet = None
        self.month = None
        self.fiscal_year = None

    def generate_excel(self, file_name):
        """Generate and export Excel file"""
        if not os.path.exists(self.TEMPLATE_FILE):
            frappe.throw(_("GSTR 3B Excel template not found"))

        excel = ExcelExporter(file=self.TEMPLATE_FILE)
        self._update_worksheet(excel)

        excel.export(file_name)

    def _update_worksheet(self, excel):
        self.worksheet = excel.wb[self.WORKSHEET_NAME]

        self._set_header_info()
        self._set_outward_supplies()
        self._set_ecommerce_supplies()
        self._set_inter_state_supplies()
        self._set_itc_details()
        self._set_inward_supplies()

    def _set_header_info(self):
        """Set header information"""
        period = self.data.get("ret_period", "")
        if not period or len(period) < 6:
            return

        try:
            month_num = int(period[:2])
            calendar_year = int(period[2:6])
        except ValueError:
            return

        self.month = calendar.month_name[month_num]
        self.fiscal_year = self._get_fiscal_year(month_num, calendar_year)

        self._set_cell(self.ROWS["gstin"], self.HEADER_COLUMNS["gstin"], self.gstin)
        self._set_cell(self.ROWS["year"], self.HEADER_COLUMNS["year"], self.fiscal_year)
        self._set_cell(self.ROWS["month"], self.HEADER_COLUMNS["month"], self.month)

    def _get_fiscal_year(self, month_num, calendar_year):
        if month_num >= 4:
            fiscal_year_start = str(calendar_year)
            fiscal_year_end = str(calendar_year + 1)[2:]
        else:
            fiscal_year_start = str(calendar_year - 1)
            fiscal_year_end = str(calendar_year)[2:]

        return f"{fiscal_year_start}-{fiscal_year_end}"

    def _set_outward_supplies(self):
        sup_details = self.data.get("sup_details", {})

        section_mappings = [
            ("osup_det", "tax"),
            ("osup_zero", "zero_rated"),
            ("osup_nil_exmp", "taxable_only"),
            ("isup_rev", "tax"),
            ("osup_nongst", "taxable_only"),
        ]

        for json_key, column_set in section_mappings:
            data = sup_details.get(json_key, {})
            self._set_section_data(json_key, data, column_set)

    def _set_ecommerce_supplies(self):
        eco_dtls = self.data.get("eco_dtls", {})
        self._set_section_data("eco_reg_sup", eco_dtls.get("eco_reg_sup", {}), "taxable_only")

    def _set_inter_state_supplies(self):
        inter_sup = self.data.get("inter_sup", {})
        pos_data = self._group_by_place_of_supply(inter_sup)

        if not pos_data:
            return

        max_rows = len(self._STATE_CODE_TO_NAME)
        for i, (pos, data) in enumerate(sorted(pos_data.items())):
            if i >= max_rows:
                break
            row = self.ROWS["inter_state_start"] + i
            self._set_inter_state_row(row, pos, data)

    def _group_by_place_of_supply(self, inter_sup):
        pos_data = {}
        categories = {
            "unreg_details": "unreg",
            "comp_details": "comp",
            "uin_details": "uin",
        }

        for category_key, category_name in categories.items():
            for item in inter_sup.get(category_key, []):
                state_code = item.get("pos", "00")
                state_name = self._format_place_of_supply(state_code)

                if state_name not in pos_data:
                    pos_data[state_name] = {
                        "unreg": {"txval": 0, "iamt": 0},
                        "comp": {"txval": 0, "iamt": 0},
                        "uin": {"txval": 0, "iamt": 0},
                    }

                pos_data[state_name][category_name]["txval"] += flt(item.get("txval", 0), 2)
                pos_data[state_name][category_name]["iamt"] += flt(item.get("iamt", 0), 2)

        return pos_data

    def _set_inter_state_row(self, row, pos, data):
        self._set_cell(row, 2, pos)

        categories = [
            ("unreg", 3, 4),
            ("comp", 5, 6),
            ("uin", 7, 8),
        ]

        for category, val_col, tax_col in categories:
            category_data = data.get(category, {"txval": 0, "iamt": 0})
            self._set_cell(row, val_col, category_data["txval"])
            self._set_cell(row, tax_col, category_data["iamt"])

    def _set_itc_details(self):
        itc_elg = self.data.get("itc_elg", {})
        self._populate_itc_sections(itc_elg.get("itc_avl", []), self.ITC_AVAILABLE_TYPES)
        self._populate_itc_sections(itc_elg.get("itc_rev", []), self.ITC_REVERSED_TYPES)
        self._populate_itc_sections(
            itc_elg.get("itc_inelg", []), self.ITC_INELIGIBLE_TYPES
        )

    def _populate_itc_sections(self, itc_entries, type_mapping):
        for itc_entry in itc_entries:
            itc_type = itc_entry.get("ty", "")
            if itc_type not in type_mapping:
                continue

            row_key = type_mapping[itc_type]
            column_set = "import_itc" if itc_type in ["IMPG", "IMPS"] else "itc"
            self._set_section_data(row_key, itc_entry, column_set, self.ITC_COLUMNS)

    def _set_inward_supplies(self):
        inward_sup = self.data.get("inward_sup", {})
        isup_details = inward_sup.get("isup_details", [])

        for supply_data in isup_details:
            supply_type = supply_data.get("ty")
            if supply_type in self.INWARD_SUPPLY_TYPES:
                row_key = self.INWARD_SUPPLY_TYPES[supply_type]
                self._set_section_data(row_key, supply_data, "inward", self.INWARD_COLUMNS)

    def _set_section_data(self, row_key, data, column_set, columns_dict=None):
        row = self.ROWS[row_key]
        columns = self.COLUMN_SETS[column_set]
        mapping = columns_dict or self.TAX_COLUMNS

        for key in columns:
            if key in mapping:
                value = flt(data.get(key, 0), 2)
                self._set_cell(row, mapping[key], value)

    def _set_cell(self, row, column, value):
        cell = self.worksheet.cell(row, column)
        if isinstance(cell, MergedCell):
            return
        # Preserve template formulas (e.g. SGST = CGST mirror cells);
        # only write to plain-value cells.
        if isinstance(cell.value, str) and cell.value.startswith("="):
            return
        cell.value = value

    @classmethod
    def _format_place_of_supply(cls, state_code):
        formatted_code = state_code.zfill(2)
        state_name = cls._STATE_CODE_TO_NAME.get(formatted_code, "Other Territory")
        return f"{formatted_code}-{state_name}"
