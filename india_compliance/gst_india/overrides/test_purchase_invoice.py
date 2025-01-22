import frappe
from frappe.tests.utils import FrappeTestCase, change_settings
from erpnext.accounts.doctype.account.test_account import create_account

from india_compliance.gst_india.utils.tests import append_item, create_purchase_invoice


class TestPurchaseInvoice(FrappeTestCase):
    @change_settings("GST Settings", {"enable_overseas_transactions": 1})
    def test_itc_classification(self):
        pinv = create_purchase_invoice(
            supplier="_Test Foreign Supplier",
            do_not_submit=1,
            item_code="_Test Service Item",
        )
        self.assertEqual(pinv.itc_classification, "Import Of Service")

        append_item(pinv)
        pinv.save()
        self.assertEqual(pinv.itc_classification, "Import Of Goods")

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

    def test_purchase_invoice_taxes_TC_ACC_075(self):
        from india_compliance.gst_india.doctype.gst_hsn_code.gst_hsn_code import update_taxes_in_item_master
        from frappe.utils import today
        # Step 1: Create GST HSN Code with Taxes
        taxes = [{"item_tax_template": "GST 18% - _TIRC", "tax_category": "In-State"}]
        hsn_code = "100100"

        # Create GST HSN Code
        if not frappe.db.exists("GST HSN Code", hsn_code):
            hsn_doc = frappe.get_doc(
                {"doctype": "GST HSN Code", "hsn_code": hsn_code, "taxes": taxes}
            )
            hsn_doc.save()

        # Create Item with GST HSN Code
        item_code = "SKU8899"
        if not frappe.db.exists("Item", item_code):
            
            item = frappe.get_doc(
                {
                    "doctype": "Item",
                    "item_code": item_code,
                    "item_group": "All Item Groups",
                    "gst_hsn_code": hsn_code,
                    "stock_uom": "Nos",
                }
            )
            item.save()

        # Update taxes in item master
        update_taxes_in_item_master(taxes=taxes, hsn_code=hsn_code)

        # Validate the item has correct tax template
        self.assertDocumentEqual(taxes[0], frappe.get_doc("Item", item_code).taxes[0])

        # Step 2: Setup Company and Vendor with GSTIN
        company = "_Test Indian Registered Company"
        vendor = "_Test Registered Supplier"

        # Step 3: Create Purchase Invoice
        purchase_invoice = frappe.new_doc("Purchase Invoice")
        purchase_invoice.company = company
        purchase_invoice.supplier = vendor
        purchase_invoice.append(
            "items",
            {
                "item_code": item_code,
                "qty": 1,
                "rate": 100,
                "gst_hsn_code": hsn_code,
            },
        )
        
        taxes_and_charges = frappe.call(
            "erpnext.accounts.party.get_party_details",
            party=vendor,
            party_type="Supplier",
            account= "Creditors - _TIRC",
            company=company,
            posting_date = today()
        ).get("taxes_and_charges")
        # Set the taxes_and_charges in the Purchase Invoice
        purchase_invoice.taxes_and_charges = taxes_and_charges
        purchase_invoice.bill_no = "XXX-01"
        purchase_invoice.save()
        # Step 4: Validate Taxes in Purchase Invoice
        taxes_in_invoice = purchase_invoice.get("taxes")
        self.assertGreater(len(taxes_in_invoice), 0, "Taxes should be fetched for the Purchase Invoice.")

        # # Validate tax accounts
        for tax in taxes_in_invoice:
            self.assertIn(
                tax.account_head,
                ["Input Tax CGST - _TIRC", "Input Tax SGST - _TIRC"],
                "Tax account should match GST rules based on In-State or Out-State classification.",
            )

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
            pinv.save,
        )
