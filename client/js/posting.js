$(function() {
	$(document).on("click", "#send", function(ev) {
		$.post('post', {"subject": $("#update").val(), "date": (new Date()).toString()}, function(data) {
			if (data["error"]) {
				// some kind of feedback here regarding the error
				$("#update").css("border", "1px solid red");
			} else {
				if (data["posted"] && data["posted"] && data["posted"]["codes"] && data["posted"]["codes"].indexOf("APPENDUID") != -1) {
					// hooray the post was successful
					$("#update").val("");
					$("#update").css("border", null);
				} else {
					// unspecified error - log or show it
					$("#update").css("border", "1px solid red");
				}
			}
		}, 'json');
	});
});