Install
-------

Choose one of the installation methods below, depending on your requirements.

### Apache webserver

 * Install Django-1.4.1
 * Install python-gnupg
 * Check out the source code into a folder e.g. /var/www/YOUR-DOMAIN/dorcx
 * Do `git submodule init && git submodule update` in the dorcx folder
 * Install one of the Apache configs
 * Restart Apache

### Gunicorn

	$ cd server
	$ make gunicorn

### Local development

	git clone 
	git submodule init
	git submodule update
	cd server
	./manage.py runserver

Then visit http://127.0.0.1:8000/ in your browser.

