// when the app is first loaded in the browser this code runs
$(function() {
	// in error.js always catch errors that come back via ajax and display the message
	catch_ajax_errors($("#messages"));
	
	// once the templates are loaded
	$(document).bind("templates_loaded", function(ev) {
		// test to see if this client is already authenticated
		$.get("authenticate", function(data) {
			// hide the default loader
			$("#messages").html("");
			// if the server says we're not logged in
			// or there is a problem with the authentication details
			if (data == false || data["error"]) {
				// show the user the login form
				$("#content").html(template["login-form.html"]);
				// redirect error messages to where the user will more easily see them
				catch_ajax_errors($("#login-messages"));
			} else {
				// otherwise load up the main interface
				_dorcx_main();
			}
		}, "json");
	});
	
	/***
		Login/setup process 
	***/
	
	// if they click the 'more options' button on the login form expose the details
	$(document).on("click", "#login-form-more-options", function(ev) {
		ev.preventDefault();
		$("#login-form-extra-details").show();
		$(this).hide();
	});
	
	// when the login form is submitted
	$(document).on("submit", "#login-form", function(ev) {
		// stop form from submitting normally
		ev.preventDefault();
		
		// clear any existing error messages
		$("#login-messages").html("");
		
		// disable the submit button
		$('#login-form-submit').hide();
		// show the ajax loader next to the submit button
		$("#login-form-submit-loader").show();
		// remove any pending error messages
		$("#errors").html("");
		
		// trigger the post
		$.post($(this).attr("action"), $(this).serialize(), function(data) {
			console.log(data);
			if (data["error"]) {
				// display the extra form fields to allow more detail.
				$("#login-form-extra-details").show();
				// re-enable the submit button and loader
				$("#login-form-submit-loader").hide();
				$('#login-form-submit').show();
			} else {
				// load up the main interface
				_dorcx_main();
			}
		}, "json").error(function() {
			// re-enable the submit button and loader
			$("#login-form-submit-loader").hide();
			$('#login-form-submit').show();
		});
		
		return false;
	});
});
