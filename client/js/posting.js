$(function() {
	$(document).on("click", "#send", function(ev) {
		if ($("#update").val()) {
			$("#send").html("<i class='icon-spinner icon-spin'></i>");
			$.post('post', {"subject": $("#update").val(), "date": (new Date()).toString()}, function(data) {
				$("#send").html("Update");
				if (data["error"]) {
					// some kind of feedback here regarding the error
					$("#update").removeClass("error");
				} else {
					if (data["posted"] && data["posted"] && data["posted"]["codes"] && data["posted"]["codes"].indexOf("APPENDUID") != -1) {
						// hooray the post was successful
						$("#update").val("");
						$("#update").removeClass("error");
					} else {
						// unspecified error - log or show it
						$("#update").addClass("error");
					}
				}
			}, 'json');
		} else {
			$("#update").addClass("error");
		}
		ev.preventDefault();
	});
});
