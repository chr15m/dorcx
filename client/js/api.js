// code to communicate with the back-end
$(function() {
	// when the login form is submitted
	$(document).on("submit", "#login-form", function(ev) {
		// stop form from submitting normally
		ev.preventDefault();
		
		// disable the submit button and show a loader
		$('input[type=submit]', this).attr('disabled', 'disabled');
		$("#login-form-submit-loader").show();
		
		// trigger the post
		$.post($(this).attr("action"), $(this).serialize(), function(data) {
			console.log(data);
			if (data["error"]) {
				// display the error and the extra form fields to allow more detail.
				$("#login-error").html(_dorcx_lookup_error(data));
				$("#login-form-extra-details").show();
				// re-enable the submit button and loader
				$("#login-form-submit-loader").hide();
				$("#login-form-submit").attr('disabled', null);
			} else {
				// show the next page of the process
				$("#content").html(template["signed-in-setup-folders.html"]);
			}
		}, "json");
				
		return false;
	});
	
	
});
