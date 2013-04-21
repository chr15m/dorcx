from json_encode import json_api

from imapdb import ImapDb, ImapDbException

class LoginError(Exception):
	pass

@json_api
def signin(request):
	try:
		if request.method == "POST":
			d = ImapDb(request.POST.get("email"), request.POST.get("password"), request.POST.get("username"), request.POST.get("domain"), request.POST.get("use_ssl", True))
			return d.get_missing_folder_list()
		else:
			return {"error": ["BAD-PROTOCOL"]}
	except ImapDbException, e:
		return {"error": e.message}

