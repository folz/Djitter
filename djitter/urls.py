from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Djitter (?P<link>.{40})
	
	url(r'^$', 'djweet.views.home', name='home'),
	
	url(r'(?P<username>\w+)$', 'djweet.views.view', name='view'),
	
	url(r'edit/$', 'djweet.views.edit', name='edit'),
	
	url(r'publish/$', 'djweet.views.publish_chirp', name='publish'),
	
	url(r'follow/(?P<username>\w+)/$', 'djweet.views.follow', name='follow'),
	
	
	# django-registration
	
	url(r'^accounts/', include('registration.urls')),
	
	url(r'^accounts/profile/$', 'djweet.views.back_to_home', name='redir'),
	
	
	# Django Admin
	
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	url(r'^admin/', include(admin.site.urls)),
)
