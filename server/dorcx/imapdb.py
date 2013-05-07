#!/usr/bin/python

import imaplib
import re
import socket
from email.parser import HeaderParser
from email.utils import getaddresses

total_re = re.compile("MESSAGES (?P<total>\d+)")
unread_re = re.compile("UNSEEN (?P<unread>\d+)")

BASIC_EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

FOLDERS = ["dorcx/", "dorcx/config", "dorcx/inbox", "dorcx/public/", "dorcx/public/config", "dorcx/public/outbox", "dorcx/private/", "dorcx/private/config", "dorcx/private/outbox"]

# TODO: persist multiple imap connections in some sensible way
# TODO: unit tests

total_re = re.compile("MESSAGES (?P<total>\d+)")
unread_re = re.compile("UNSEEN (?P<unread>\d+)")

class ImapDbException(Exception):
	pass

class ImapDb:
	""" Communicates with the current user's IMAP box, manages the dorcx contents, treats an IMAP mailbox like a database. """
	def __init__(self, email, password, username=None, domain=None, use_ssl=True):
		# validate email
		if BASIC_EMAIL_REGEX.match(email):
			emailparts = email.split("@")
		else:
			raise ImapDbException(["EMAIL-VALIDATION"])
		# get the username from the email address
		if not username:
			username = emailparts[0]
		# get the domain name from the email address
		if not domain:
			domain = emailparts[1]
		# TODO: on failure automatically try various ways of connecting (Non-SSL, common server subdomains, etc.)
		# try to connect to the IMAP server
		# TODO: timeout? if you incorrectly connect to some servers with no SSL they hang
		try:
			if use_ssl:
				self.m = imaplib.IMAP4_SSL(domain)
			else:
				self.m = imaplib.IMAP4(domain)
		except socket.gaierror, e:
			raise ImapDbException(["CONNECTION", e.message])
		except socket.error, e:
			raise ImapDbException(["CONNECTION", e.message])
		# TODO: arg? ImapDbException: ['AUTH', 'Maximum number of connections from user+IP exceeded (mail_max_userip_connections)']
		# try to log in with the username and password provided
		try:
			self.m.login(username, password)
		except self.m.error, e:
			raise ImapDbException(["AUTH", e.message])
	
	def get_missing_folder_list(self):
		result = self.m.list("dorcx*")
		""" 	In [4]: d.m.list("dorcx*")
			Out[4]: 
			('OK',
			 ['(\\Noselect \\HasChildren) "/" "dorcx"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/inbox"',
			  '(\\Noselect \\HasChildren) "/" "dorcx/public"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/public/outbox"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/public/config"',
			  '(\\Noselect \\HasChildren) "/" "dorcx/private"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/private/outbox"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/private/config"',
			  '(\\NoInferiors \\UnMarked) "/" "dorcx/config"'])"""
		# see if the folders we want match those on the server
		want = set([f.rstrip("/") for f in FOLDERS])
		have = set(folder_names_from_folder_list(result))
		need = list(want - have)
		return {"missing_folders": need, "all_missing": len(need) == len(FOLDERS)}
	
	def setup_folders(self):
		""" Sets up the dorcx subfolder and its subfolders - config, private, public. """
		results = []
		for d in FOLDERS:
			result = self.m.create(d)
			# if there was an error result ("NO") and there were errors other than "ALREADYEXISTS" errors then throw
			if result and len(result) and result[0] == 'NO' and len([r for r in result[1] if "ALREADYEXISTS" in r]) != len(result[1]):
				raise ImapDbException(["BOX-CREATION", result])
			else:
				results.append([d, result])
		return {"created_folders": results}
	
	def get_unread_count(self, boxes=['INBOX']):
		""" Returns unread count for the user's actual INBOX folder. """
		try:
			for b in boxes:
				r = self.m.status(b, '(UNSEEN MESSAGES)')[1][0]
				total = total_re.search(r)
				unread = unread_re.search(r)
				yield b,[unread, total and total.groupdict()["total"] or 0, unread and unread.groupdict()["unread"] or 0]
		except socket.gaierror, e:
			raise ImapDbException(["INBOX-READ", e.message])
	
	def get_folder_list(self):
		# filter out undesireable folder names, dorcx folders, and hidden folders
		return [f for f in folder_names_from_folder_list(self.m.list()) if not (
			f.lower() in ["trash", "templates", "drafts", "spam", "junk"]
			or f.startswith("dorcx")
			or f.startswith(".")
		)]
	
	def get_headers(self, folder, number):
		print folder, number
		self.m.select(folder, readonly=True)
		msgs = []
		count = int(self.get_unread_count([folder]).next()[1][1])
		print count
		# unread = unread_re.search(r).groupdict()["unread"]
		for i in range(1, min(number, count)):
			print "fetching", i
			data = self.m.fetch(str(i), '(BODY[HEADER])')
			header_data = data[1][0][1]
			parser = HeaderParser()
			msgs.append(parser.parsestr(header_data))
		return msgs
	
def people_from_header(msg):
	# parse the realnames and emails out of various fields of a message
	return getaddresses(
		msg.get_all('to', []) +
		msg.get_all('cc', []) +
		msg.get_all('from', []) + 
		msg.get_all('resent-to', []) +
		msg.get_all('resent-cc', []) +
		msg.get_all('envelope-to', [])
	)

def folder_names_from_folder_list(flist):
	return [f.split(" ")[-1][1:-1] for f in flist[1]]
