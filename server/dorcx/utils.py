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
			return {"error": e.message}
	return new_fn

