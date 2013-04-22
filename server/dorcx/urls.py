from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

import settings

urlpatterns = patterns('',
	# Serve the index page
	url(r'^$', direct_to_template, {"template": "client/index.html"}, name='home'),
	
	# JSON API endpoings
	url(r'^signin$', "dorcx.views.signin", name="signin"),
	url(r'^create-missing-folders$', "dorcx.views.create_missing_folders", name="create_missing_folders"),
	url(r'^authenticate$', "dorcx.views.authenticate", name="authenticate"),
	
	# Examples:
	# url(r'^$', 'dorcx.views.home', name='home'),
	# url(r'^dorcx/', include('dorcx.foo.urls')),

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

