// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Member', {
	// refresh: function(frm) {
  refresh: function(frm) {
       frm.add_custom_button('Create Membership', () => {
           frappe.new_doc('Library Membership', {
               library_member: frm.doc.name
           })
       })
       frm.add_custom_button('Create Log', () => {
           frappe.new_doc('Library Log', {
               customer_id: frm.doc.name
           })
       })
   }
	// }
});
