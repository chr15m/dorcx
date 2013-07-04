#!/usr/bin/python

import re
import socket
import dateutil.parser
import email
from email.parser import HeaderParser
from email.utils import getaddresses
from email.message import Message
from datetime import datetime

from imapclient import IMAPClient

# TODO: persist multiple imap connections in some sensible way (check out imap proxys like perdition)
# TODO: unit tests

basic_email_re = re.compile(r"[^@]+@[^@]+\.[^@]+")
plus_email_re = re.compile("\+.*\@")
noreply_email_re = re.compile(".*?not{0,1}.{0,1}reply@.*?", flags=re.IGNORECASE)
append_response_re = re.compile("\[(?P<codes>.*)\] \({0,1}(?P<message>.*)\){0,1}$", flags=re.IGNORECASE)

class ImapDbException(Exception):
	pass

class ImapDb(IMAPClient):
	""" Communicates with the current user's IMAP box, manages the dorcx contents, treats an IMAP mailbox like a database. """
	def __init__(self, email, password, username=None, domain=None, use_ssl=True):
		# validate email
		if basic_email_re.match(email):
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
		IMAPClient.__init__(self, domain, use_uid=True, ssl=use_ssl)
		# try to log in with the username and password provided
		try:
			self.login(username, password)
		# IMAPClient.Error
		except Exception, e:
			raise ImapDbException(["AUTH", e.message])
		# cache the capabilities of the server we're connecting to
		self.capabilities()
		# store these useful variables for later
		self.email = email
		self.username = username
		self.domain = domain
		# figure out which folder listing algorithm to use
		# ** Gmail have deprecated XLIST but this code might be useful on some servers later **
		# self.list_folders = ("XLIST" in self.capabilities() and self.xlist_folders or self.list_folders)
	
	def get_dorcx_folder_list(self):
		return self.list_folders("dorcx/%")
	
	def get_rich_folder_list(self):
		""" Return the good, content rich folders in this user's mailbox if they are named as e.g. INBOX, Archive, etc. or if they have a special flag saying they are useful. """
		return [f[2] for f in self.list_folders() if f[2].lower() in [
			"sent",
			"inbox",
			"archive",
			"archives",
			"important",
			"sent mail",
			"[gmail]/sent mail",
			"[gmail]/starred",
			"[gmail]/important",
			"[gmail]/all mail",
			"all mail"
		] or len(
			[x for x in ("\\All", "\\Sent", "\\Flagged", "\\Important") if x in f[0]]
		)]
	
	def get_messages(self, message_ids):
		response = self.fetch(message_ids, ['RFC822', 'FLAGS'])
		messages = {}
		for msgid, data in response.iteritems():
			msg_string = data['RFC822']
			if not u'\\Deleted' in data['FLAGS']:
				msg = email.message_from_string(msg_string)
				messages[msgid] = msg
		return messages
	
	def list_folder(self, folder, dorcx_folder=False):
		# choose the folder we want to list
		self.select_folder((dorcx_folder and "dorcx/" or "") + folder, readonly=True)
		# fetch a list of all message IDs in this mailbox
		return self.search(["NOT DELETED"])
	
	def get_headers(self, folder, number):
		messages = self.list_folder(folder)
		# now just pop the headers of the last number of them
		all_headers = self.fetch(messages[-number:], ['BODY[HEADER]', 'UID'] + ("X-GM-EXT-1" in self.capabilities() and ['X-GM-MSGID', 'X-GM-THRID'] or []))
		# parse them all and return
		for h in all_headers:
			all_headers[h]["header"] = HeaderParser().parsestr(all_headers[h]["BODY[HEADER]"])
			all_headers[h]["UID"] = h
		return all_headers
	
	def get_threads(self, folder, number):
		threads = []
		# fetch all the recent rich headers
		headers = self.get_headers(folder, number)
		# now cruise through them finding ones that are between multiple people
		for h in headers:
			p = remove_noreplies(remove_duplicate_people(exclude_email(people_from_header(headers[h]["header"]), self.email)))
			if len(p) > 1 and not "list-id" in [k.lower() for k in headers[h]["header"].keys()]:
				threads.append(headers[h])
		# sort the messages by date
		threads.sort(lambda a,b: cmp(a["header"]["Date"], b["header"]["Date"]))
		return threads
	
	def post(self, folder, subject="", body="", date=None, metadata=None):
		folder_name = "dorcx/" + folder
		# test if the folder exists already
		folder_exists = len(self.list_folders(folder_name))
		if not folder_exists:
			# create it if it does not yet exist
			result = self.create_folder(folder_name)
			# In [10]: g.create_folder("dorcx/public")
			# Out[10]: u'Success'
			
			# In [13]: i.create_folder("dorcx/public")
			# Out[13]: u'Create completed.'

			# In [9]: g.create_folder("dorcx/")
			# Out[9]: u'[CANNOT] Ignoring hierarchy declaration (Success)'
			
			# fail raises:
			# error: create failed: u'[ALREADYEXISTS] Mailbox exists.'
		# now choose the folder so we can write our new post to it
		self.select_folder(folder_name, readonly=False)
		# create the post as a new email
		m = Message()
		m["From"] = self.email
		# m["To"] = "public@dorcx.net"
		m["Content-Type"] = "text/plain"
		if subject:
			m["Subject"] = subject
		# Javascript should use d.toString() = "Sun Jun 09 2013 16:21:47 GMT+0800 (WST)"
		msg_time = (date and dateutil.parser.parse(date) or None)
		if msg_time:
			# Date - 
			# djb nails it:
			# http://cr.yp.to/immhf/date.html
			# Date: 23 Dec 1995 19:25:43 -0000
			m["Date"] = msg_time.strftime("%a, %d %b %Y %X %z")
		if body:
			m.set_payload(body)
		response = self.append(folder_name, m.as_string(), msg_time=msg_time)
		#print response
		# u'[APPENDUID 594556012 1] (Success)'
		# u'[APPENDUID 1370766584 11] Append completed.'
		result = {"message": None, "codes": []}
		if append_response_re.match(response):
			result = append_response_re.match(response).groupdict()
			result["codes"] = result["codes"].split(" ")
		return result, m

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

def exclude_email(email_list, check):
	return [e for e in email_list if plus_email_re.sub("@", e[1]).lower() != check.lower()]

def remove_duplicate_people(email_list):
	emails_only = [e[1] for e in email_list]
	no_dup_list = []
	for e in email_list:
		if not e[1] in [d[1] for d in no_dup_list]:
			no_dup_list.append(e)
	return no_dup_list

def remove_noreplies(email_list):
	return [e for e in email_list if noreply_email_re.match(e[1]) is None]
