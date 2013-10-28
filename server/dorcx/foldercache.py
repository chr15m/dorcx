from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404

import dateutil.parser

from dorcx.models import LongCacheItem
from django.utils import feedgenerator

from dorcx.utils import email_md5

class FolderCache:
	""" Cache of messages by message ID. """
	def __init__(self, foldername, email=None, md5ed_email=None):
		if email:
			md5ed_email = email_md5(email)
			self.email = email
		else:
			self.email = None
		self.foldername = foldername
		self.key = "foldercache-" + md5ed_email + "-" + foldername
	
	def get_or_create_cache(self):
		self.cache, created = LongCacheItem.objects.get_or_create(key=self.key)
		# if we have an empty message cache start by initialising it
		if not self.cache.value:
			self.cache.value = {"email": self.email, "posts": {}, "uids_by_date": [], "last": "1/1/1978 00:00:00 +0000"}
			self.cache.save()
		return self.cache
	
	def get_cache_or_404(self):
		self.cache = get_object_or_404(LongCacheItem, key=self.key)
		return self.cache
	
	def synchronise(self, connection):
		cache = self.get_or_create_cache()
		# figure out which messages are in our cache and which are missing
		need_message_uids = set(connection.list_folder(self.foldername))
		have_message_uids = set(cache.value["posts"].keys())
		extra = have_message_uids - need_message_uids
		missing = need_message_uids - have_message_uids
		# remove the ones we don't need any more from the cache
		for e in extra:
			del cache.value["posts"][e]
		# grab the new ones and put them in our cache
		cache.value["posts"].update(connection.get_messages(missing))
		# sort the post UIDs by date of the post
		def todate(c, u):
			return dateutil.parser.parse(c.value["posts"][u].get("Date", "1/1/1978 00:00:00 +0000"))
		cache.value["uids_by_date"] = sorted(self.cache.value["posts"].keys(), lambda a, b: cmp(todate(cache, b), todate(cache, a)))
		# date of the last post
		if len(cache.value.get("uids_by_date", [])):
			cache.value["last"] = cache.value["posts"][cache.value["uids_by_date"][0]]["Date"]
		else:
			return "1/1/1978 00:00:00 +0000"
		cache.save()

class FolderCacheFeed(Feed):
	feed_type = feedgenerator.Rss201rev2Feed
	
	def get_object(self, request, email_hash, foldername):
		self.email_hash = email_hash
		self.foldername = foldername
		return FolderCache(foldername, md5ed_email=email_hash).get_cache_or_404()
	
	### feed level ###
	
	def title(self, obj):
		return "dorcx/" + self.foldername + "/" + obj.value["email"]
	
	def description(self, obj):
		return self.foldername + " dorcx feed for " + obj.value["email"]
	
	def link(self, obj):
		return "/post/" + self.email_hash + "/" + self.foldername + "/"
	
	### item level ###
	
	def items(self, obj):
		return [{"post": obj.value["posts"][p], "uid": p} for p in obj.value["uids_by_date"]]
	
	def item_title(self, item):
		return item["post"]["Subject"]
	
	def item_description(self, item):
		return item["post"].get_payload()
	
	def item_link(self, item):
		return "/post/" + self.email_hash + "/" + self.foldername + "/" + str(item["uid"])
	
	def item_pubdate(self, item):
		if item["post"].get("Date"):
			dateutil.parser.parse(item["post"]["Date"])
	
	# TODO: append host also	
	# def item_guid(self, obj):
	# item_guid_is_permalink = True

