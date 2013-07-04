from md5 import md5
from email.utils import parseaddr

from django.contrib.auth import logout

import settings

from json_encode import json_api

from utils import login, catch_imapdb_errors
from feedcache import FeedCache
from imapdb import people_from_header, ImapDbException

@json_api
@catch_imapdb_errors
def signin(request):
	if request.method == "POST":
		# save the login details in this user's session for future server commands
		request.session["login_details"] = request.POST
		d = login(request)
		return d.capabilities()
	else:
		return {"error": ["BAD-PROTOCOL"]}

@json_api
def signout(request):
	del request.session["login_details"]
	request.session.flush()
	logout(request)
	return True

@json_api
@catch_imapdb_errors
def create_missing_folders(request):
	d = login(request)
	return d.setup_folders()

@json_api
@catch_imapdb_errors
def authenticate(request):
	""" Simple test to see if the current session is authenticated or not. """
	if request.session.get("login_details") is None:
		return False
	else:
		try:
			d = login(request)
		except ImapDbException:
			return False
		return True

@json_api
@catch_imapdb_errors
def get_contacts(request):
	# d = login(request)
	return []

@json_api
@catch_imapdb_errors
def find_new_contacts(request):
	contacts = []
	contacts_by_email = {}
	d = login(request)
	# get a list of folders we can search through
	# TODO search more folders than these ones in some kind of asynchronous way
	folders = [f for f in d.get_rich_folder_list()]
	for f in folders:
		# get the first 100 headers of each folder
		for m in d.get_headers(f, settings.MESSAGE_HISTORY_CACHE_SIZE):
			# TODO: cull out lists using X-List header
			people = people_from_header(m)
			for p in people:
				if contacts_by_email.has_key(p[1]):
					contacts_by_email[p[1]]["count"] += 1
				else:
					contacts.append({
						"folder": f,
						"email": p[1],
						"name": p[0],
						"count": 1
					})
					contacts_by_email[p[1]] = contacts[-1]
	contacts.sort(lambda a, b: cmp(b["count"], a["count"]))
	return contacts

@json_api
@catch_imapdb_errors
def get_threads(request):
	threads =[]
	d = login(request)
	folders = [f for f in d.get_rich_folder_list()]
	for f in folders:
		for m in d.get_threads(f, settings.MESSAGE_HISTORY_CACHE_SIZE):
			header = m["header"]
			people = people_from_header(header)
			threads.append({
				"name": parseaddr(header["From"])[0],
				"email": parseaddr(header["From"])[1],
				"people": [{"name": p[0], "email": p[1]} for p in people],
				"subject": header["Subject"],
				"date": header["Date"],
				"uid": m.get("X-GM-MSGID", m["UID"]),
				"raw_header": m["BODY[HEADER]"]
			})
	return threads

@json_api
@catch_imapdb_errors
def post(request):
	# post_type = request.POST.get("post-type")
	body = request.POST.get("body")
	subject = request.POST.get("subject")
	date = request.POST.get("date")
	folder = "public"
	# date = request.POST.get("date")
	if body or subject:
		d = login(request)
		# make the actual post into our 'imapdb'
		result, message = d.post(folder, subject, body, date)
		# update the cache of messages we keep server side for this user in this folder
		FeedCache(folder, email=d.email).synchronise(d)
		return {"posted": result}
	else:
		return {"error": "No body or subject supplied."}
