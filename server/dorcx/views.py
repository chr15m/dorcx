from md5 import md5

from django.contrib.auth import logout

from json_encode import json_api

from utils import login, catch_imapdb_errors

from imapdb import people_from_header

@json_api
@catch_imapdb_errors
def signin(request):
	if request.method == "POST":
		# save the login details in this user's session for future server commands
		request.session["login_details"] = request.POST
		d = login(request)
		return d.get_missing_folder_list()
	else:
		return {"error": ["BAD-PROTOCOL"]}

@json_api
def signout(request):
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
	if request.session.get("login_details") is None:
		return False
	else:
		d = login(request)
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
		for m in d.get_headers(f, 30):
			print m
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

