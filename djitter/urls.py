from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Djitter
	url(r'^$', 'djweet.views.Index', name='index'),
	url(r'profile/(\d+)/$', 'djweet.views.ViewProfile', name='profile'),
	url(r'editprofile/$', 'djweet.views.EditProfile', name='edit'),
	url(r'publish/$', 'djweet.views.PublishChirp', name='publish'),
	url(r'follow/(\d+)/$', 'djweet.views.FollowUser', name='follow'),
	url(r'unfollow/(\d+)/$', 'djweet.views.UnfollowUser', name='unfollow'),
	
	# Django-Registration
	url(r'^accounts/', include('registration.backends.default.urls')),
	
	# Django Admin
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
