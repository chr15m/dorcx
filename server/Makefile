
runserver: vp
	vp/bin/python manage.py runserver

runserver_plus: vp
	vp/bin/python manage.py runserver_plus

vp:
	virtualenv vp
	vp/bin/pip install -r requirements.txt

gunicorn: vp
	vp/bin/gunicorn_django -w 5 -t 15 dorcx
