var _dorcx_error_messages = {
	"CONNECTION": "There was a problem contacting the server. Did you enter the correct server details?",
	"AUTH": "There was a problem logging in. Did you enter the right password?",
	"BOX-CREATION": "There was a problem creating the dorcx folders in your email box.",
	"INBOX-READ": "There was a problem communicating with your email box.",
	"EMAIL-VALIDATION": "You have not entered a valid email address.",
	"BAD-PROTOCOL": "Couldn't log in. Are you using the latest version?"
}

function _dorcx_lookup_error(e) {
	var error_code = e["error"][0];
	if (error_code) {
		return _dorcx_error_messages[error_code];
	} else {
		return "Oops, some error occured we can't figure out.";
	}
}
