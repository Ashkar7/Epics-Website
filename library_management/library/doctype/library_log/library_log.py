# Copyright (c) 2022, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import date_diff, getdate
from frappe.model.document import Document
import re
from datetime import datetime
from datetime import date, timedelta
class LibraryLog(Document):
	def validate(self):
		if (self.issued_book_log and len(self.issued_book_log)>3):
			frappe.throw('Book Issue Limit Exceeded')
		book_status(self)
		self.extented_date = date_diff(self.submission_date, self.due_date)
		self.due_date = getdate(self.borrower_date) + timedelta(days=7)
		if getdate(self.submission_date) < getdate(self.due_date):
			self.fine_amount_per_day = 0
			self.total_fine_amount = 0
		elif self.fine_amount_per_day and self.extented_date:
			self.total_fine_amount = self.fine_amount_per_day * self.extented_date
	# def after_save(self):
	# 	print("\n sdfghjk \n")
	# 	book_status(self)

	def on_submit(self):
		update_issued_quantity(self)
		add_issued_books(self)
		remove_issued_books(self)
		remove_issued_book_log(self)
		book_condition(self)


		# member_issued_details(self)

	def before_insert(self):
		add_issued_book_log(self)

	def before_save(self):
		mrp = frappe.db.get_value('Library Article', {'name':self.article}, ['mrp'])
		if mrp:
			self.fine_amount_per_day = mrp * .05
def book_condition(self):

	mrp = frappe.db.get_value('Library Article', {'name':self.article}, ['mrp'])
	if self.book_condition == "20% Damage":
		self.total_fine_amount = self.total_fine_amount + mrp * .1
	elif self.book_condition == "Reject":
		self.total_fine_amount = mrp


def update_issued_quantity(self):
	# article_doc = frappe.get_doc({'doctype':'Library Article','name':self.article})
	article_doc_name = frappe.db.get_value('Library Article',{'name':self.article},['name'])
	article_doc = frappe.get_doc('Library Article',article_doc_name)
	if self.purpose == "Issue":
		article_doc.issued_quantity = article_doc.issued_quantity + 1
	else:
		article_doc.issued_quantity = article_doc.issued_quantity - 1
	article_doc.save()

def	payment_status(self):
	if self.purpose == "Issue":
		if frappe.db.exists("Library Membership",{'library_member':self.customer},):
			membership_doc_name = frappe.db.get_value('Library Membership',{'library_member':self.customer,"from_date": ("<", self.borrower_date),"to_date": (">", self.borrower_date)},['name'])
			membership_doc = frappe.get_doc('Library Membership',membership_doc_name)
			if membership_doc:
				if not membership_doc.paid:
					frappe.throw("Payment Pending")


def borrower_date(self):
	membership_doc_name = frappe.db.get_value('Library Membership',{'full_name':self.customer},['name'])
	membership_doc = frappe.get_doc('Library Membership',membership_doc_name)
	if not (getdate(self.borrower_date) >= getdate(membership_doc.from_date) and getdate(self.borrower_date) < getdate(membership_doc.to_date)):
		frappe.throw("Membership Not Valid!!!!")

def add_issued_book_log(self):
	if self.purpose == "Issue":
		issued_book_log_row = self.append('issued_book_log')
		issued_book_log_row.article = self.article
		issued_book_log_row.issued_date = self.borrower_date
		frappe.msgprint(msg='<b> '+ self.article +'</b> Book Issued.', alert=True)

def add_issued_books(self):
	if self.purpose == "Issue":
		membership_doc = frappe.get_doc('Library Membership',self.customer_id)
		issued_books_row = membership_doc.append('issued_books')
		issued_books_row.article = self.article
		issued_books_row.library_log = self.name
		issued_books_row.issued_date = self.borrower_date
		membership_doc.save()
		frappe.msgprint(msg='<b> '+ self.article +'</b> Book Issued.', alert=True)

@frappe.whitelist()
def fetch_issued_book_log(membership):
	membership_doc = frappe.get_doc('Library Membership', membership)
	if membership_doc.issued_books:
		return membership_doc.issued_books
	else:
		return []

def remove_issued_books(self):
	if self.purpose == "Return":
		for item in self.issued_book_log :
			if item.article == self.article:
				self.remove(item)
				self.save()
def book_status(self):
	if self.purpose =="Issue" and self.issued_book_log :
		membership_doc = frappe.get_doc('Library Membership',self.customer_id)
		for item in membership_doc.issued_books:
			if self.article == item.article:
				frappe.throw("Book is Already Held by The Customer")				# self.refresh()

def remove_issued_book_log(self):
	if self.purpose == "Return":
		membership_doc = frappe.get_doc('Library Membership',self.customer_id)
		for item in membership_doc.issued_books:
			if item.article == self.article:
				membership_doc.remove(item)
				membership_doc.save()
@frappe.whitelist()
def list_location(article):
	doc = frappe.get_doc("Library Article", article);
	return doc.book_location
