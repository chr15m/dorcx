var _dorcx_error_messages = {
	"CONNECTION": "There was a problem contacting the server. Did you enter the correct server details?",
	"AUTH": "There was a problem logging in. Did you enter the right password?",
	"BOX-CREATION": "There was a problem creating the dorcx folders in your email box.",
	"INBOX-READ": "There was a problem communicating with your email box.",
	"EMAIL-VALIDATION": "You have not entered a valid email address.",
	"BAD-PROTOCOL": "Couldn't log in. Are you using the latest version?",
	"SOCKET": "We can't connect to your email server."
}

function _dorcx_lookup_error(e) {
	var error_code = e["error"][0];
	if (error_code) {
		return _dorcx_error_messages[error_code];
	} else {
		return "Oops, some error occured that we can't figure out.";
	}
}

function add_error_message(msg) {
	var error_message = $(Mustache.render(template["error.html"], {"message": msg}));
	// if the error message is clicked dissapear it
	error_message.click(function() {
		$(this).hide().remove();
	});
	$("#messages").append(error_message);
	return error_message;
}

function catch_ajax_errors() {
	// if we receive a genuine ajax error then report it
	$(document).ajaxError(function(ev, request, settings) {
		add_error_message("Sorry, there was a problem contacting the server.");
	});
	
	// check all messages coming back from the server for the 'error' key and display
	$(document).ajaxComplete(function(ev, request, settings) {
		if (settings["dataType"] == "json") {
			var data = $.parseJSON(request.responseText);
			if (data["error"]) {
				add_error_message(_dorcx_lookup_error(data));
			}
		}
	});
}
