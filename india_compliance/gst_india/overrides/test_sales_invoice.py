import unittest

import frappe

from india_compliance.gst_india.utils import validate_invoice_number
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from frappe.tests.utils import change_settings

class TestSalesInvoice(unittest.TestCase):
    def test_validate_invoice_number(self):
        posting_date = "2021-05-01"

        invalid_names = [
            "SI$1231",
            "012345678901234567",
            "SI 2020 05",
            "SI.2020.0001",
            "PI2021 - 001",
        ]
        for name in invalid_names:
            doc = frappe._dict(
                name=name, posting_date=posting_date, doctype="Sales Invoice"
            )
            self.assertRaises(frappe.ValidationError, validate_invoice_number, doc)

        valid_names = [
            "012345678901236",
            "SI/2020/0001",
            "SI/2020-0001",
            "2020-PI-0001",
            "PI2020-0001",
        ]
        for name in valid_names:
            doc = frappe._dict(name=name, posting_date=posting_date)
            try:
                validate_invoice_number(doc)
            except frappe.ValidationError:
                self.fail("Valid name {} throwing error".format(name))

    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_sales_invoice_with_sez_customer_TC_ACC_074(self):
        # Change customer GST category to SEZ
        customer = frappe.get_doc("Customer", "_Test NC")
        customer.gstin = "27AABCS4225M2Z6"
        customer.gst_category = "SEZ"
        customer.save()

        # Create Sales Invoice
        si = create_sales_invoice(
            company="_Test Indian Registered Company",
            customer="_Test NC",
            warehouse="Stores - _TIRC",
            cost_center="Main - _TIRC",
            selling_price_list="Standard Selling",
            income_account="Sales - _TIRC",
            expense_account="Cost of Goods Sold - _TIRC",
            debit_to="Debtors - _TIRC",
            qty=4,
            rate=5000,
            do_not_save=True
        )

        si.save().submit()

        # Assertions for Sales Invoice
        self.assertEqual(si.status, "Unpaid", "Sales Invoice submission failed")
        self.assertEqual(si.grand_total, si.total + si.total_taxes_and_charges, "Grand total calculation mismatch")
        self.assertEqual(si.total_taxes_and_charges, 0, "Total tax amount mismatch for SEZ customer")


    def test_sales_invoice_with_gst_TC_ACC_076(self):
        # Create Sales Invoice
        si = create_sales_invoice(
            company="_Test Indian Registered Company",
            customer="_Test Registered Customer",
            warehouse="Stores - _TIRC",
            cost_center="Main - _TIRC",
            selling_price_list="Standard Selling",
            income_account="Sales - _TIRC",
            expense_account="Cost of Goods Sold - _TIRC",
            debit_to="Debtors - _TIRC",
            qty=4,
            rate=5000,
            do_not_save=True
        )

        # Map tax category and address details
        si.tax_category = "In-State"
        si.taxes_and_charges = "Output GST In-state - _TIRC"

        # Save and submit the Sales Invoice
        si.save().submit()

        # Validate tax amounts and rates
        total_tax_rate = 18  # Assuming GST (CGST + SGST) is 18%
        total_taxable_value = si.total
        expected_tax_amount = (total_taxable_value * total_tax_rate) / 100
        sgst_rate = 9  # Assuming CGST and SGST are split equally
        cgst_rate = 9

        # Fetch taxes applied on the Sales Invoice
        taxes = si.taxes

        self.assertEqual(len(taxes), 2, "Expected 2 tax rows (CGST and SGST)")

        for tax in taxes:
            if tax.account_head == "Output Tax SGST - _TIRC":
                self.assertEqual(tax.rate, sgst_rate, "SGST rate mismatch")
                self.assertEqual(tax.tax_amount, expected_tax_amount / 2, "SGST amount mismatch")
            elif tax.account_head == "Output Tax CGST - _TIRC":
                self.assertEqual(tax.rate, cgst_rate, "CGST rate mismatch")
                self.assertEqual(tax.tax_amount, expected_tax_amount / 2, "CGST amount mismatch")
            else:
                self.fail(f"Unexpected tax account {tax.account_head}")

        # Validate total tax amounts
        self.assertEqual(si.total_taxes_and_charges, expected_tax_amount, "Total tax amount mismatch")