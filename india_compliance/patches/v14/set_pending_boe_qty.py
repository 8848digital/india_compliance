import frappe
from frappe.query_builder import Case


def execute():
    pi_item = frappe.qb.DocType("Purchase Invoice Item")
    boe_item = frappe.qb.DocType("Bill of Entry Item")

    (
        frappe.qb.update(pi_item)
        .set(
            pi_item.pending_boe_qty,
            Case()
            .when(((boe_item.name.isnotnull()) & (boe_item.docstatus == 1)), 0)
            .else_(pi_item.qty),
        )
        .from_(boe_item)
        .where(boe_item.pi_detail == pi_item.name)
        .run()
    )