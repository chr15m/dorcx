// when the app is first loaded in the browser this code runs
$(function() {
	// in error.js always catch errors that come back via ajax and display the message
	catch_ajax_errors();
	
	// once the templates are loaded
	$(document).bind("templates_loaded", function(ev) {
		// test to see if this client is already authenticated
		$.get("authenticate", function(data) {
			// if the server says we're not logged in
			// or there is a problem with the authentication details
			if (data == false || data["error"]) {
				// start the login process
				$("#loader").hide();
				$("#content").html(template["login-form.html"]);
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
		
		// disable the submit button
		$('input[type=submit]', this).attr('disabled', 'disabled');
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
				$("#login-form-submit").attr('disabled', null);
			} else {
				// load up the main interface
				_dorcx_main();
			}
		}, "json").error(function() {
			// re-enable the submit button and loader
			$("#login-form-submit-loader").hide();
			$("#login-form-submit").attr('disabled', null);
		});
		
		return false;
	});
	
	$(document).on("click", "#setup-folders-yes", function(ev) {
		// ask the server to create any missing folders for this user
		$.get("create-missing-folders", function(data) {
			console.log(data);
			// load up the main interface
			_dorcx_main();
		}, "json");
	});
	
	$(document).on("click", "#setup-folders-no", function(ev) {
		// show the k thx bai screen
		$("#content").html(template["do-not-continue.html"]);
	});
	
});
