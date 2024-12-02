import frappe
from frappe.query_builder.functions import IfNull


def execute():
    if frappe.db.db_type == "postgres":
        # Update Purchase Invoice reconciliation status to "Not Applicable"
        frappe.db.sql(
            """
            UPDATE "tabPurchase Invoice" AS pi
            SET reconciliation_status = 'Not Applicable'
            FROM "tabPurchase Invoice Item" AS pii
            WHERE pi.name = pii.parent
            AND pi.docstatus = 1
            AND (
                COALESCE(pi.supplier_gstin, '') = ''
                OR COALESCE(pi.gst_category, '') IN ('Registered Composition', 'Unregistered', 'Overseas')
                OR COALESCE(pi.supplier_gstin, '') = pi.company_gstin
                OR COALESCE(pi.is_opening, '') = 'Yes'
                OR pii.gst_treatment = 'Non-GST'
            )
            """
        )

        # Update Purchase Invoice reconciliation status to "Unreconciled"
        frappe.db.sql(
            """
            UPDATE "tabPurchase Invoice"
            SET reconciliation_status = 'Unreconciled'
            WHERE docstatus = 1
            AND COALESCE(reconciliation_status, '') = ''
            """
        )

        # Update Bill of Entry reconciliation status to "Unreconciled"
        frappe.db.sql(
            """
            UPDATE "tabBill of Entry"
            SET reconciliation_status = 'Unreconciled'
            WHERE docstatus = 1
            """
        )

    else:
        PI = frappe.qb.DocType("Purchase Invoice")
        PI_ITEM = frappe.qb.DocType("Purchase Invoice Item")
        BOE = frappe.qb.DocType("Bill of Entry")

        (
            frappe.qb.update(PI)
            .set(PI.reconciliation_status, "Not Applicable")
            .join(PI_ITEM)
            .on(PI.name == PI_ITEM.parent)
            .where(PI.docstatus == 1)
            .where(
                (IfNull(PI.supplier_gstin, "") == "")
                | (
                    IfNull(PI.gst_category, "").isin(
                        ["Registered Composition", "Unregistered", "Overseas"]
                    )
                )
                | (IfNull(PI.supplier_gstin, "") == PI.company_gstin)
                | (IfNull(PI.is_opening, "") == "Yes")
                | (PI_ITEM.gst_treatment == "Non-GST")
            )
            .run()
        )

        (
            frappe.qb.update(PI)
            .set(PI.reconciliation_status, "Unreconciled")
            .where(PI.docstatus == 1)
            .where(IfNull(PI.reconciliation_status, "") == "")
            .run()
        )

        (
            frappe.qb.update(BOE)
            .set(BOE.reconciliation_status, "Unreconciled")
            .where(BOE.docstatus == 1)
            .run()
        )
