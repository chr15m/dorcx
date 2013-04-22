from json_encode import json_api

from utils import login, catch_imapdb_errors

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

