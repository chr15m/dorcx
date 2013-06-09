function _dorcx_main() {
	// show the main interface
	$("#content").html(Mustache.render(template["main.html"], {}, {"posting": template["posting.html"]}));
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
	
	$("#new-contacts").html("");
	// initiate the check for new contacts
	/*$.get("find-new-contacts", function(contacts) {
		console.log(contacts);
		// clear out the existing list
		$("#new-contacts").html("");
		// fill the new-contacts box with the contacts we have found
		for (var c=0; c<contacts.length; c++) {
			var contact = contacts[c];
			var contacthtml = $(Mustache.render(template["contact.html"], contacts[c]));
			$("#new-contacts").append(contacthtml);
			
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
		});
	}, "json");*/
	
	// initiate a download of all threads
	$.get("get-threads", function(threads) {
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
	}, "json");
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

