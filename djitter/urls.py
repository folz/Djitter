from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Djitter (?P<link>.{40})
	url(r'^$', 'djweet.views.index', name='index'),
	url(r'editprofile/$', 'djweet.views.edit_profile', name='edit'),
	url(r'publish/$', 'djweet.views.publish_chirp', name='publish'),
	url(r'follow/(?P<user>\w+)/$', 'djweet.views.follow_user', name='follow'),
	url(r'unfollow/(?P<user>\w+)/$', 'djweet.views.unfollow_user', name='unfollow'),
	url(r'(?P<user>\w+)/?$', 'djweet.views.view_profile', name='profile'),
	
	# Django-Registration
	url(r'^accounts/', include('registration.urls')),
	
	# Django Admin
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
