from dorcx.models import LongCacheItem
from dorcx.utils import email_md5

class FeedCache:
	""" Cache of messages by message ID. """
	def __init__(self, email, foldername):
		self.email = email
		self.foldername = foldername
		self.key = "feedcache-" + email_md5(email) + "-" + foldername
		self.cache, created = LongCacheItem.objects.get_or_create(key=self.key)
		# if we have an empty message cache start by initialising it
		if not self.cache.value:
			self.cache.value = {}
			self.cache.save()
	
	def synchronise(self, connection):
		# figure out which messages are in our cache and which are missing
		need_message_uids = set(connection.list_folder(self.foldername, True))
		have_message_uids = set(self.cache.value.keys())
		extra = have_message_uids - need_message_uids
		missing = need_message_uids - have_message_uids
		# remove the ones we don't need any more from the cache
		for e in extra:
			del self.cache.value[e]
		# grab the new ones and put them in our cache
		self.cache.value.update(connection.get_messages(missing))
		self.cache.save()
