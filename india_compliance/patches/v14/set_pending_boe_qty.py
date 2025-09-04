import frappe
from frappe.query_builder.functions import IfNull, Sum


def execute():
    pi = frappe.qb.DocType("Purchase Invoice")
    pi_item = frappe.qb.DocType("Purchase Invoice Item")
    boe_item = frappe.qb.DocType("Bill of Entry Item")

    submitted_boe_qty = (
        frappe.qb.from_(boe_item)
        .select(boe_item.pi_detail, fn.Sum(boe_item.qty).as_("qty"))
        .where(boe_item.docstatus == 1)
        .groupby(boe_item.pi_detail)
    ).as_("submitted_boe_qty")

    query = (
        frappe.qb.update(pi_item)
        .set( 
            pi_item.pending_boe_qty,
            pi_item.qty - fn.Coalesce(submitted_boe_qty.qty, 0),
        )
        .from_(pi)                       
        .from_(submitted_boe_qty)        
        .where(pi_item.parent == pi.name)
        .where(pi.docstatus == 1)
        .where(pi.gst_category == "Overseas")
        .where(pi_item.name == submitted_boe_qty.pi_detail)  
    )

    query.run()
    
    
    
    