// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Article', {
issued_quantity:function(frm){
  frm.set_value("remaining_quantity",cur_frm.doc.stock-cur_frm.doc.issued_quantity)
}
});

frappe.ui.form.on('Book Location', {
  section: function(frm,cdt,cdn) {
    var d=locals[cdt][cdn]
  frappe.model.set_value(d.doctype,d.name,"article_location",(d.journer).slice(0,3)+"-"+d.rack+"-"+d.row+"-"+d.section)

  }
	// refresh: function(frm) {

	// }
});
