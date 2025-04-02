import frappe


def execute():
    boe_item = frappe.qb.DocType("Bill of Entry Item")
    boe = frappe.qb.DocType("Bill of Entry")

    if frappe.db.db_type == "postgres":
        (
            frappe.qb.update(boe_item)
            .set(boe_item.purchase_invoice, boe.purchase_invoice)
            .from_(boe)
            .where(boe_item.parent == boe.name)
            .run()
        )
    else:
        (
            frappe.qb.update(boe_item)
            .join(boe)
            .on(boe_item.parent == boe.name)
            .set(boe_item.purchase_invoice, boe.purchase_invoice)
            .run(as_dict=True)
        )
