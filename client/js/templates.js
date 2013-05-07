// global variable to store the template files
var template = {};

var _dorcx_template_files = [
	"login-form.html",
	"signed-in-setup-folders.html",
	"do-not-continue.html",
	"need-more-folders.html",
	"contact.html",
	"signed-out.html",
	"main.html"
];

$(function() {
	// load the templates
	for (t=0; t<_dorcx_template_files.length; t++) {
		$.get("c/templates/" + _dorcx_template_files[t], function(tn, t) {
			return function(data) {
				template[tn] = data;
				_dorcx_template_files.pop();
				// once we've loaded each template
				if (_dorcx_template_files.length == 0) {
					$(document).trigger('templates_loaded');
				}
			}
		}(_dorcx_template_files[t], t));
	}
});
