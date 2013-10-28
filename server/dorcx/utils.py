import md5
import socket
import json

from imapdb import ImapDb, ImapDbException

def login(request):
	""" Performs a login with the server details of this user that have been stored in their session. """
	login_details = request.session.get("login_details", {})
	return ImapDb(login_details.get("email"), login_details.get("password"), login_details.get("username"), login_details.get("domain"), login_details.get("use_ssl", True))

def catch_imapdb_errors(fn):
	""" Decorator to automatically return any imapdb errors as JSON to the client. """
	def new_fn(request, *args, **kwargs):
		try:
			return fn(request, *args, **kwargs)
		except ImapDbException, e:
			if not hasattr(e, "messages") or len(e.messages) and e.messages[0] == "AUTH":
				del request.session["login_details"]
			return {"error": e.message}
		except socket.gaierror, e:
			del request.session["login_details"]
			return {"error": ["SOCKET", "We can't connect to your mail server."]}
	return new_fn

def email_md5(email):
	return md5.new("dorcx:" + email).hexdigest()

