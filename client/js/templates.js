// global variable to store the template files
var template = {};

$(function() {
	// load the templates
	var template_files = ["login-form.html"];
	for (t=0; t<template_files.length; t++) {
		$.get("c/templates/" + template_files[t], function(tn, t) {
			return function(data) {
				template[tn] = data;
				template_files.pop();
				// once we've loaded each template
				if (template_files.length == 0) {
					$(document).trigger('templates_loaded');
				}
			}
		}(template_files[t], t));
	}
});
