// code to manage the user interface
$(function() {
	// once the templates are loaded hide the loader and show the login form
	$(document).bind("templates_loaded", function(ev) {
		$("#loader").hide();
		$("#content").html(template["login-form.html"]);
	});
});
