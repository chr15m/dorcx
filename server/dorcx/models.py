from django.db import models
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
from picklefield.fields import PickledObjectField

class LongCacheItem(models.Model):
	"""
		Django model for storing cached items for a long time in the database.
		In dorcx this is used by the server to cache your outgoing IMAP feeds so people can see them when they hit the server.
		Anything non-public should be encrypted by your key anyway so this shouldn't be much of a security risk.
	"""
	key = models.CharField(max_length=1024)
	value = PickledObjectField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

#class LongCacheItemIndex(models.Model):
#	""" Used by the LongCache to index on certain things - free text field or a link to a specific object. """
#	cacheitem = models.ForeignKey(LongCacheItem)
#	created = models.DateTimeField(auto_now_add=True)
#	updated = models.DateTimeField(auto_now=True)
#	name = models.CharField(max_length=1024)
#	value = models.TextField()
#	# can optionally link to an object
#	content_type = models.ForeignKey(ContentType)
#	object_id = models.PositiveIntegerField()
#	content_object = generic.GenericForeignKey('content_type', 'object_id')
#
#	def __unicode__(self):
#		return self.name
