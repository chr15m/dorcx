from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template
from django.core.validators import email_re

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from dorcx.feedcache import FeedCacheFeed

import settings

urlpatterns = patterns('',
	# Serve the index page
	url(r'^$', direct_to_template, {"template": "client/index.html"}, name='home'),
	
	# JSON API endpoints
	url(r'^signin$', "dorcx.views.signin", name="signin"),
	url(r'^signout$', "dorcx.views.signout", name="signout"),
	url(r'^authenticate$', "dorcx.views.authenticate", name="authenticate"),
	url(r'^get-contacts$', "dorcx.views.get_contacts", name="get_contacts"),
	url(r'^find-new-contacts$', "dorcx.views.find_new_contacts", name="find_new_contacts"),
	url(r'^get-threads$', "dorcx.views.get_threads", name="get_threads"),
	url(r'^post$', "dorcx.views.post", name="post"),
	
	# RSS API endpoints
	(r'^feed/(?P<email_hash>[a-zA-Z0-9]{32})/(?P<foldername>.*?).rss$', FeedCacheFeed()),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	# Uncomment the next line to enable the admin:
	# url(r'^admin/', include(admin.site.urls)),
)

# statically serve this stuff while developing
if settings.DEBUG:
	urlpatterns += static("/c/", document_root=settings.CLIENT_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

