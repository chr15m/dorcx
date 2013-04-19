from json_encode import json_api

from imapdb import ImapDb, ImapDbException

class LoginError(Exception):
	pass

@json_api
def signin(request):
	try:
		if request.method == "POST":
			d = ImapDb(request.POST.get("email"), request.POST.get("password"), request.POST.get("username"), request.POST.get("domain"), request.POST.get("use_ssl"))
		else:
			return {"error": "Couldn't log in. Are you using the latest version?"}
	except ImapDbException, e:
		return {"error": e.message}

