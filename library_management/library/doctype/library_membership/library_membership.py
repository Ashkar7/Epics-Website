# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
# from frappe.model.docstatus import DocStatus

class LibraryMembership(Document):
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": 1,
                # check if the membership's end date is later than this membership's start date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")
