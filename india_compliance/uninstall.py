import click
import json
import os
import frappe
from india_compliance.gst_india.constants import BUG_REPORT_URL
from india_compliance.gst_india.uninstall import before_uninstall as remove_gst
from india_compliance.gst_india.uninstall import (
    delete_education_custom_fields,
    delete_healthcare_custom_fields,
    delete_hrms_custom_fields,
)
from india_compliance.income_tax_india.uninstall import (
    before_uninstall as remove_income_tax,
)


def before_uninstall():
    try:
        print("Removing Income Tax customizations...")
        remove_income_tax()

        print("Removing GST customizations...")
        remove_gst()

        print("Removing GST Rate...")
        remove_item_tax_template_test_records()

        print("Removing GST HSN Code...")
        remove_item_gst_hsn_code_from_test_records()

    except Exception as e:
        click.secho(
            (
                "Removing customizations for India Compliance failed due to an error."
                " Please try again or"
                f" report the issue on {BUG_REPORT_URL} if not resolved."
            ),
            fg="bright_red",
        )
        raise e


def before_app_uninstall(app_name):
    if app_name == "hrms":
        delete_hrms_custom_fields()

    if app_name == "education":
        delete_education_custom_fields()
    
    if app_name == "healthcare":
        delete_healthcare_custom_fields()

def remove_item_tax_template_test_records():

    # Path to the test records file
    test_records_path = frappe.get_app_path("erpnext", "accounts", "doctype", "item_tax_template", "test_records.json")
    
    # Step 1: Load existing test records
    try:
        with open(test_records_path, "r") as file:
            test_records = json.load(file)
    except FileNotFoundError:
        frappe.throw(f"File not found: {test_records_path}")
        return

    # Step 2: Remove the 'gst_rate' key from each record
    for record in test_records:
        record.pop("gst_rate", None)  # Safely remove if it exists

    # Step 3: Save the updated records back to the file
    with open(test_records_path, "w") as file:
        json.dump(test_records, file, indent=4)

    frappe.msgprint("gst_rate field removed from test records successfully.")

def remove_item_gst_hsn_code_from_test_records():
    import json
    import frappe

    # Path to the test records file
    test_records_path = frappe.get_app_path("erpnext", "stock", "doctype", "item", "test_records.json")

    # Step 1: Load the existing test records
    try:
        with open(test_records_path, "r") as file:
            test_records = json.load(file)
    except FileNotFoundError:
        frappe.throw(f"File not found: {test_records_path}")
        return

    # Step 2: Remove 'gst_hsn_code' field from each record
    for record in test_records:
        record.pop("gst_hsn_code", None)  # Safe removal

    # Step 3: Write the updated records back to the file
    with open(test_records_path, "w") as file:
        json.dump(test_records, file, indent=4)

    frappe.msgprint("gst_hsn_code removed from item test records.")
