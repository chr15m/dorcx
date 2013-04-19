#!/usr/bin/python

import imaplib
import re
import socket

total_re = re.compile("MESSAGES (?P<total>\d+)")
unread_re = re.compile("UNSEEN (?P<unread>\d+)")

# TODO: persist multiple imap connections in some sensible way
class ImapDb:
	def __init__(self, email, password, username=None, domain=None):
		# TODO: validate email first
		emailparts = email.split("@")
		# get the username from the email address
		if username is None:
			username = emailparts[0]
		# get the domain name from the email address
		if domain is None:
			domain = emailparts[1]
		# TODO: test various ways of logging in (Non-SSL), common server subdomains, etc.
		# TODO: catch e.g. socket.gaierror: [Errno -2] Name or service not known
		self.m = imaplib.IMAP4_SSL(domain)
		# TODO: catch e.g. imaplib.error: [AUTHENTICATIONFAILED] Authentication failed.
		self.m.login(username, password)
	
	def setup_folders(self):
		""" Sets up the dorcx subfolder and it's subfolders - config, private, public. """
		# TODO: catch errors properly
		# TODO: ignore this error though:
		# ('NO', ['[ALREADYEXISTS] Mailbox exists.'])
		result = self.m.create("dorcx/")
		if result and len(result) and result[0] == 'NO':
			return {"error": result}
		else:
			self.m.create("dorcx/config")
			self.m.create("dorcx/inbox")
			self.m.create("dorcx/public/")
			self.m.create("dorcx/public/config")
			self.m.create("dorcx/public/outbox")
			self.m.create("dorcx/private/")
			self.m.create("dorcx/private/config")
			self.m.create("dorcx/private/outbox")
			return True
	
	def get_unread_count(self, boxes=[]):
		""" Returns unread count for the user's actual INBOX folder. """
		try:
			for b in ['INBOX'] + boxes:
				r = self.m.status(b, '(UNSEEN MESSAGES)')[1][0]
				total = total_re.search(r).groupdict()["total"]
				unread = unread_re.search(r).groupdict()["unread"]
				return [unread, total]
		except socket.gaierror, e:
			return {"error": e}

