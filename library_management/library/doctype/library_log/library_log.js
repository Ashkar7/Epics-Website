// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Log', {
	article: function(frm) {
		if (frm.doc.article){
			frappe.call({
				method: "library_management.library.doctype.library_log.library_log.list_location",
				args:{
					article:frm.doc.article
				},
				callback(r){
					if (r){
						var d =" "
						r.message.ForEach((i)=>{
							d+="\n"+i.article_location
						})
						frm.set_df_property("article_location","options",d)
						frm.refresh_field("article_location")
					}
				}
			})
		}
	},
	refresh: function(frm) {
    frm.set_query('issue_log', () => {
        return {
            filters: {
                purpose: 'Issue',
								customer: frm.doc.customer,
                name: ['!=', frm.doc.name ]
            }
        }
    })
		if (frm.doc.purpose=='Issue'){
			frm.set_query('article', () => {
	        return {
	            filters: {
	                remaining_quantity: ['!=', 0 ]
	            }
	        }
	    })
		}
	},
	// after_save: function(frm) {
	// 	validate_issued_book_log(frm);
	// },
	customer_id: function(frm){
		if(frm.doc.customer_id){
			fetch_issued_book_log(frm);
		}
	}
});

// function validate_issued_book_log(frm){
// 	if (frm.doc.issued_book_log && frm.doc.issued_book_log.length>3){
// 		frappe.throw(__('Book Issue Limit Exceeded'));
// 	}
// }

function fetch_issued_book_log(frm){
	if(frm.doc.customer_id){
		frappe.call({
			method: "library_management.library.doctype.library_log.library_log.fetch_issued_book_log",
			args:{
				membership:frm.doc.customer_id
			},
			callback(r){
				if (r && r.message){
					r.message.forEach(function(issued_book) {
						let row = frm.add_child('issued_book_log', {
							article : issued_book.article,
							issued_date : issued_book.issued_date ,
						});
					});
					frm.refresh_field('issued_book_log');
				}
			},
			freeze: true,
			freeze_message: ('Fetching Issued Books from Membership.!!')
		});
	}
}
