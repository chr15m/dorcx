function _dorcx_main() {
	// show the main interface
	$("#content").html(template["main.html"]);
	$("#loader").hide();
	
	// hook up the 'sign out' button
	$("#sign-out").click(function(ev) {
		$.get("signout", function(data) {
			$("#content").html(template["signed-out.html"]);
		}, "json");
	});
	
	// load up my existing contacts
	$.get("get-contacts", function(data) {
		$("#existing-contacts").html("");
	}, "json");
	
	// initiate the check for new contacts
	$.get("find-new-contacts", function(contacts) {
		console.log(contacts);
		// clear out the existing list
		$("#new-contacts").html("");
		// fill the new-contacts box with the contacts we have found
		for (var c=0; c<contacts.length; c++) {
			$("#new-contacts").append(Mustache.render(template["contact.html"], contacts[c]));
		}
	}, "json");
}
