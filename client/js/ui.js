// code to manage the user interface
$(function() {
	// once the templates are loaded hide the loader and show the login form
	$(document).bind("templates_loaded", function(ev) {
		$("#loader").hide();
		$("#content").html(template["login-form.html"]);
	});
	
	/*** Login/setup process ***/
	$(document).on("click", "#setup-folders-yes", function(ev) {
		
	});
	
	$(document).on("click", "#setup-folders-no", function(ev) {
		$("#content").html(template["do-not-continue.html"]);
	});
	
});
