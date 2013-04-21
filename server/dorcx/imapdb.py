#!/usr/bin/python

import imaplib
import re
import socket

total_re = re.compile("MESSAGES (?P<total>\d+)")
unread_re = re.compile("UNSEEN (?P<unread>\d+)")

BASIC_EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# TODO: persist multiple imap connections in some sensible way

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
		# try to log in with the username and password provided
		try:
			self.m.login(username, password)
		except self.m.error, e:
			raise ImapDbException(["AUTH", e.message])
	
	def setup_folders(self):
		""" Sets up the dorcx subfolder and its subfolders - config, private, public. """
		default_folders = ["dorcx/", "dorcx/config", "dorcx/inbox", "dorcx/public/", "dorcx/public/config", "dorcx/public/outbox", "dorcx/private/", "dorcx/private/config", "dorcx/private/outbox"]
		results = []
		for d in default_folders:
			result = self.m.create("dorcx/")
			# if there was an error result ("NO") and there were errors other than "ALREADYEXISTS" errors then throw
			if result and len(result) and result[0] == 'NO' and len([r for r in result[1] if "ALREADYEXISTS" in r]) == len(result[1]):
				raise ImapDbException(["BOX-CREATION"])
			else:
				results.append(result)
		return results
	
	def get_unread_count(self, boxes=[]):
		""" Returns unread count for the user's actual INBOX folder. """
		try:
			for b in ['INBOX'] + boxes:
				r = self.m.status(b, '(UNSEEN MESSAGES)')[1][0]
				total = total_re.search(r).groupdict()["total"]
				unread = unread_re.search(r).groupdict()["unread"]
				yield b,[unread, total]
		except socket.gaierror, e:
			raise ImapDbException(["INBOX-READ", e.message])

