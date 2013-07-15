_dorcx_active_loaders = {};

function add_loader(name, msg) {
	var progress_element = $(Mustache.render(template["loader.html"], {"message": msg}));
	$("#messages").append(progress_element);
	_dorcx_active_loaders[name] = progress_element;
	return progress_element;
}

function del_loader(name) {
	_dorcx_active_loaders[name].hide().remove();
}
