from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	
	# Djitter (?P<link>.{40})
	
	url(r'^$', 'chirp.views.home', name='home'),
	
	url(r'user/(?P<username>\w+)*', 'chirp.views.view', name='view'),
	
	url(r'edit/$', 'chirp.views.edit', name='edit'),
	
	url(r'publish/$', 'chirp.views.cheep', name='cheep'),
	
	url(r'follow/(?P<username>\w+)/$', 'chirp.views.follow', name='follow'),
	
	url(r'connect/$', 'chirp.views.connect', name='connect'),
	
	url(r'discover/$', 'chirp.views.discover', name='discover'),
	
	
	# django-registration
	
	url(r'^accounts/', include('registration.urls')),
	
	url(r'^accounts/profile/$', 'chirp.views.back_to_home', name='redir'),
	
	
	# Django Admin
	
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	
	url(r'^admin/', include(admin.site.urls)),
)
