// code to communicate with the back-end
$(function() {
	// when the login form is submitted
	$(document).on("submit", "#login-form", function(ev) {
		// stop form from submitting normally
		ev.preventDefault();
		
		// trigger the post
		$.post($(this).attr("action"), $(this).serialize(), function(data) {
			console.log(data);
			if (data["error"]) {
				// display the error and the extra form fields to allow more detail.
				$("#login-error").html(data["error"]);
				$("#login-form-extra-details").show();
			} else {
				// show the next page of the process
				$("#content").html(template["signed-in-setup-folders.html"]);
			}
		}, "json");
				
		return false;
	});
});
