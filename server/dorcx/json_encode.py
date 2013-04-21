# http://code.google.com/p/dojango/source/browse/trunk/dojango/util/__init__.py#98
# Modified to use Django's own PythonSerializer where appropriate

from decimal import Decimal

from datetime import datetime, date, time
from time import struct_time, mktime

from django.core.serializers.python import Serializer as PythonSerializer
from django.db.models.query import QuerySet
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils.functional import Promise
from django.db.models import ImageField, FileField, Model
from django.utils import simplejson as json
from django.http import HttpResponse

def json_response(result):
	return HttpResponse(json_encode(result), mimetype="text/plain")

def json_api(fn):
	""" Wrapper to turn any function into one that acts as a JSON API endpoint. """
	def newfunc(request, *args, **kwargs):
		return json_response(fn(request, *args, **kwargs))
	return newfunc

# fake these imports from appengine and django-non-rel if they don't work.
# probably a better way to handle this.
try:
	from search.core import RelationIndexQuery
except ImportError:
	class RelationIndexQuery:
		pass

try:
	from google import appengine
except ImportError:
	class appengine:
		class ext:
			class db:
				class Model:
					pass
				class Query:
					pass

from xml.sax import SAXParseException

def json_encode(data):
	"""
	The main issues with django's default json serializer is that properties that
	had been added to an object dynamically are being ignored (and it also has 
	problems with some models).
	"""
	
	def _any(data):
		ret = None
		# Opps, we used to check if it is of type list, but that fails 
		# i.e. in the case of django.newforms.utils.ErrorList, which extends
		# the type "list". Oh man, that was a dumb mistake!
		if isinstance(data, list):
			ret = _list(data)
		elif isinstance(data, dict):
			ret = _dict(data)
		elif isinstance(data, Decimal):
			# json.dumps() cant handle Decimal
			ret = str(data)
		elif isinstance(data, Model):
			ret = _model(data)
		# here we need to encode the string as unicode (otherwise we get utf-16 in the json-response)
		elif isinstance(data, basestring):
			ret = unicode(data)
		# see http://code.djangoproject.com/ticket/5868
		elif isinstance(data, Promise):
			ret = force_unicode(data)
		elif isinstance(data, datetime):
			# For dojo.date.stamp we convert the dates to use 'T' as separator instead of space
			# i.e. 2008-01-01T10:10:10 instead of 2008-01-01 10:10:10
			ret = str(data).replace(' ', 'T')
		elif isinstance(data, date):
			ret = str(data)
		elif isinstance(data, time):
			ret = "T" + str(data)
		elif isinstance(data, struct_time):
			ret = str(datetime(*data[:6])).replace(" ", "T")
		elif isinstance(data, (QuerySet, RelationIndexQuery)):
			ret = _list(data)
		elif isinstance(data, SAXParseException):
			ret = str(data)
		elif appengine and isinstance(data, appengine.ext.db.Query):
			ret = _list(data)
		elif appengine and isinstance(data, appengine.ext.db.Model):
			ret = _googleModel(data)
		else:
			# always fallback to a string!
			ret = data
		return ret
	
	def _model(data):
		return PythonSerializer().serialize([data])[0]
	
	def _googleModel(data):
		return PythonSerializer().serialize([data])[0]
	
	def _list(data):
		ret = []
		for v in data:
			ret.append(_any(v))
		return ret
	
	def _dict(data):
		ret = {}
		for k,v in data.items():
			ret[k] = _any(v)
		return ret
	
	ret = _any(data)
	return json.dumps(ret, cls=DateTimeAwareJSONEncoder, indent=1)

