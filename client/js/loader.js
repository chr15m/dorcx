_dorcx_active_loaders = {};

function add_loader(name, msg) {
	var progress_element = $("<li class='loader-item'><img src='c/img/loader.gif'/>" + msg + "</li>");
	$("#loader").append(progress_element);
	_dorcx_active_loaders[name] = progress_element;
	return progress_element;
}

function del_loader(name) {
	_dorcx_active_loaders[name].hide().remove();
}
