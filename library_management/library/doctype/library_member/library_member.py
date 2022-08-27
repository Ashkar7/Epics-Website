# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMember(Document):
	def before_save(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
	def validate(self):
		if frappe.db.exists({"doctype": "Library Member", "user": self.user, 'docstatus': 1 }):
			frappe.throw( title='Error', msg='Already exsisting customer')
