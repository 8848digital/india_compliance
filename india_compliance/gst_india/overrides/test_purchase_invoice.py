import re

import frappe
from frappe.tests.utils import FrappeTestCase, change_settings
from frappe.utils import add_months, getdate
from erpnext.accounts.doctype.account.test_account import create_account

from india_compliance.gst_india.utils.itc_claim import (
    ITC_CLAIM_PERIOD_DEFERRED,
    format_period,
)
from india_compliance.gst_india.utils.tests import append_item, create_purchase_invoice


class TestPurchaseInvoice(FrappeTestCase):
    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_boe_applicability_auto_set_without_gst_taxes(self):
        """Import Of Goods without GST taxes → is_boe_applicable auto-set to 1."""
        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_submit=1,
        )

        self.assertEqual(pinv.itc_classification, "Import Of Goods")
        self.assertEqual(pinv.is_boe_applicable, 1)
        self.assertEqual(pinv.items[0].pending_boe_qty, pinv.items[0].qty)

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_boe_applicability_auto_set_with_gst_taxes(self):
        """Import Of Goods (SEZ) with GST taxes → is_boe_applicable auto-set to 0."""
        # Use SEZ registered supplier: has GSTIN + itc_classification = Import Of Goods
        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            do_not_save=1,
            do_not_submit=1,
            is_out_state=True,
        )
        pinv.gst_category = "SEZ"
        pinv.save()

        self.assertEqual(pinv.itc_classification, "Import Of Goods")
        self.assertEqual(pinv.is_boe_applicable, 0)
        self.assertEqual(pinv.items[0].pending_boe_qty, 0)

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_sez_goods_import_with_zero_gst_rates(self):
        """SEZ goods import should save even when GST tax rows exist with zero rates."""
        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            do_not_save=1,
            do_not_submit=1,
            is_out_state=True,
        )
        pinv.gst_category = "SEZ"

        for tax in pinv.taxes:
            tax.rate = 0

        pinv.save()

        self.assertEqual(pinv.itc_classification, "Import Of Goods")
        self.assertEqual(pinv.items[0].gst_treatment, "Taxable")
        self.assertEqual(pinv.items[0].igst_rate, 0)

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_boe_applicability_auto_uncheck_when_not_import_of_goods(self):
        """is_boe_applicable should be 0 when itc_classification is not Import Of Goods."""
        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            item_code="_Test Service Item",
            do_not_submit=1,
        )
        # Service item → itc_classification = Import Of Service → is_boe_applicable auto-set to 0
        self.assertEqual(pinv.itc_classification, "Import Of Service")
        self.assertEqual(pinv.is_boe_applicable, 0)

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_itc_classification(self):
        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_submit=1,
            item_code="_Test Service Item",
        )
        self.assertEqual(pinv.itc_classification, "Import Of Service")
        self.assertEqual(pinv.items[0].gst_treatment, "Taxable")

        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_submit=1,
        )
        self.assertEqual(pinv.itc_classification, "Import Of Goods")
        self.assertEqual(pinv.items[0].gst_treatment, "Taxable")

        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            do_not_submit=1,
            do_not_save=1,
        )
        pinv.gst_category = "SEZ"
        pinv.save()
        self.assertEqual(pinv.itc_classification, "Import Of Goods")
        self.assertEqual(pinv.items[0].gst_treatment, "Taxable")

        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            do_not_submit=1,
            do_not_save=1,
            item_code="_Test Service Item",
        )
        pinv.gst_category = "SEZ"
        pinv.save()
        self.assertEqual(pinv.itc_classification, "All Other ITC")

        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            is_reverse_charge=1,
            do_not_submit=1,
        )
        self.assertEqual(pinv.itc_classification, "ITC on Reverse Charge")

        pinv.is_reverse_charge = 0
        pinv.save()
        self.assertEqual(pinv.itc_classification, "All Other ITC")

        company = "_Test Indian Registered Company"
        account = create_account(
            account_name="Unrealized Profit",
            parent_account="Current Assets - _TIRC",
            company=company,
        )

        frappe.db.set_value(
            "Company", company, "unrealized_profit_loss_account", account
        )
        pinv = create_purchase_invoice(
            supplier="Test Internal with ISD Supplier",
            qty=-1,
            is_return=1,
        )
        self.assertEqual(pinv.itc_classification, "Input Service Distributor")

        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_save=1,
            is_reverse_charge=1,
        )

        self.assertRaisesRegex(
            frappe.exceptions.ValidationError,
            "Reverse Charge is not applicable on Import of Goods",
            pinv.save,
        )

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_service_and_goods_import_invoice_itc_classification(self):
        test_cases = (
            ("Overseas", "_Test Foreign Supplier"),
            ("SEZ", "_Test Registered Supplier"),
        )

        for gst_category, supplier in test_cases:
            pinv = create_purchase_invoice(
                supplier=supplier,
                do_not_submit=1,
                do_not_save=1,
                item_code="_Test Service Item",
            )
            pinv.gst_category = gst_category
            append_item(pinv)
            pinv.save()

            self.assertEqual(pinv.itc_classification, "Import Of Goods")
            self.assertEqual(len(pinv.items), 2)
            self.assertEqual(pinv.items[0].gst_treatment, "Taxable")
            self.assertEqual(pinv.items[1].gst_treatment, "Taxable")

    def test_validate_invoice_length(self):
        # No error for registered supplier
        pinv = create_purchase_invoice(
            supplier="_Test Registered Supplier",
            is_reverse_charge=True,
            do_not_save=True,
        )
        setattr(pinv, "__newname", "INV/2022/00001/asdfsadf")  # NOQA
        pinv.meta.autoname = "prompt"
        pinv.save()

        # Error for unregistered supplier
        pinv = create_purchase_invoice(
            supplier="_Test Unregistered Supplier",
            is_reverse_charge=True,
            do_not_save=True,
        )
        setattr(pinv, "__newname", "INV/2022/00001/asdfsadg")  # NOQA
        pinv.meta.autoname = "prompt"

        pinv.save()

        self.assertEqual(
            frappe.parse_json(frappe.message_log[-1]).get("message"),
            "Transaction Name must be 16 characters or fewer to meet GST requirements",
        )

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    @change_settings("GST Settings", {"validate_hsn_code": 0})
    def test_validate_hsn_code_for_overseas(self):
        frappe.db.set_value("Item", "_Test Service Item", "gst_hsn_code", "")
        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_submit=1,
            do_not_save=1,
            item_code="_Test Service Item",
        )

        self.assertRaisesRegex(
            frappe.exceptions.ValidationError,
            re.compile(r"^(GST HSN Code is mandatory for Overseas Purchase Invoice.*)"),
            pinv.save,
        )

        frappe.db.set_value("Item", "_Test Service Item", "gst_hsn_code", "999900")

    def test_itc_claim_period_for_unregistered_rcm(self):
        """
        For Unregistered supplier RCM, ITC Claim Period must match the posting period
        """
        from india_compliance.gst_india.utils.itc_claim import format_period

        pinv = create_purchase_invoice(
            supplier="_Test Unregistered Supplier",
            is_reverse_charge=True,
            do_not_submit=True,
        )

        posting_period = format_period(pinv.posting_date)
        self.assertEqual(pinv.itc_claim_period, posting_period)

        # Try to change itc_claim_period to a different period - should fail
        pinv.itc_claim_period = "012099"  # Different period

        self.assertRaisesRegex(
            frappe.exceptions.ValidationError,
            re.compile(
                r"ITC Claim Period must be .* for purchases from Unregistered suppliers under Reverse Charge"
            ),
            pinv.save,
        )
