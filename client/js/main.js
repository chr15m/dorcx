// data we will use all across the app - cached from the server
var dorcx = {
	"contacts": [],
	"profile": {},
	"config": {}
}

// launch the main UI
function _dorcx_main() {
	// show the main interface
	$("#content").html(Mustache.render(template["main.html"], {}, {"posting": template["posting.html"]}));
	
	// where to put the error messages on the page
	catch_ajax_errors($("#messages"));
	
	// hook up the 'sign out' button
	$("#sign-out").click(function(ev) {
		$.get("signout", function(data) {
			$("#content").html(template["signed-out.html"]);
			// clear all messages
			$("#messages").html("");
		}, "json");
		ev.preventDefault();
	});
	
	// add_loader("test one", "Test number one.");
	// add_loader("another test", "The other test.");
	// add_loader("flippin test", "Flippin' test.");
	// add_error_message("This is my error message.");
	// add_error_message("Just one more error.");
	
	// load up my existing config
	add_loader("config_loader", "Fetching config");
	$.getJSON("get-config", function(config) {
		dorcx.config = config;
		del_loader("config_loader");
	});
	
	// load up my existing contacts
	add_loader("contacts_loader", "Fetching contacts");
	$.getJSON("get-contacts", function(contacts) {
		console.log(contacts);
		dorcx.contacts = contacts;
		del_loader("contacts_loader");
		add_loader("contacts_update", "Updating contacts");
		// initiate the check for new contacts
		$.getJSON("update-contacts", function(contacts) {
			console.log(contacts);
			// TODO insert new contact data instead of wiping this out
			dorcx.contacts = contacts;
			del_loader("contacts_update");
			//$("#contacts").html("");
			/*// clear out the existing list
			$("#contacts").html("");
			// fill the new-contacts box with the contacts we have found
			for (var c=0; c<contacts.length; c++) {
				var contact = contacts[c];
				var contacthtml = $(Mustache.render(template["contact.html"], contacts[c]));
				$("#contacts").append(contacthtml);
				
				var emailparts = contact.email.split("@");
				// use the right avatar
				if (emailparts[1] == "gmail.com") {
					contact.avatar_url = get_avatar_from_service("google", emailparts[0], 128);
				} else {
					contact.avatar_url = get_avatar_from_service("gravatar", md5(contact.email), 128);
				}
				// if we get a 404 just fall back to the gravatar one
				contacthtml.find("img.avatar").error(function(ev) {
					contact.avatar_url = get_avatar_from_service("gravatar", md5(contact.email), 128);
					$(this).attr("src", contact.avatar_url);
				}).attr("src", contact.avatar_url);
			}
			// bind an error function to the avatars to just load the gravatar if all else fails
			$(document).on('error', 'img.avatar', function(ev) {
				console.log("replaced");
				this.src = get_avatar_from_service("gravatar", md5($(this).attr("email")), 128);
			});*/
		});
	});
	
	// initiate a download of all threads
	/*$.getJSON("get-threads", function(threads) {
		console.log(threads);
		// clear out the existing list of threads
		$("#threads").html("");
		// get each thread and paint it
		for (var t=0; t<threads.length; t++) {
			console.log(threads[t]);
			$("#threads").append(Mustache.render(template["thread.html"], threads[t]));
		}
		// get the correct avatars
		update_avatars($("#threads"));
	});*/
}

function update_avatars(who) {
	var avatars = $(who).find(".avatar");
	for (var a=0; a<avatars.length; a++) {
		var avatar = $(avatars[a]);
		var address = avatar.attr("email");
		var emailparts = address.split("@");
		var width = avatar.attr("width");
		// if we get a 404 just fall back to the gravatar one
		avatar.error(function(a, w) {
			return function(ev) {
				$(this).attr("src", get_avatar_from_service("gravatar", md5(a), w));
			};
		}(address, width))
		// try to use something awesome
		if (emailparts[1] == "gmail.com") {
			avatar.attr("src", get_avatar_from_service("google", emailparts[0], width));
		} else {
			avatar.attr("src", get_avatar_from_service("gravatar", md5(address), width));
		}
	}
}

