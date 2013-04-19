// code to communicate with the back-end
$(function() {
	// when the login form is submitted
	$(document).on("submit", "#login-form", function(ev) {
		// stop form from submitting normally
		ev.preventDefault();
		
		// trigger the post
		$.post($(this).attr("action"), $(this).serialize(), function(data) {
			if (data["error"]) {
				$("#login-error").html(data["error"]);
			} else {
				// next step...
			}
		}, "json");
				
		return false;
	});
});
