from django.conf.urls.defaults import patterns, include, url
from django.views.generic.create_update import *
from django.conf import settings
from views import *

# Uncomment the next two lines to enable the admin:
 from django.contrib import admin
 admin.autodiscover()

urlpatterns = patterns((r'^$', Index),
					   (r'profile/(\d+)/$', ViewProfile),
					   (r'editprofile/$', EditProfile),
					   (r'publish/$', PublishChirp),
					   (r'follow/(\d+)/$', FollowUser),
					   (r'unfollow/(\d+)/$', UnfollowUser),
					   (r'^accounts/', include('registration.backends.default.urls')),
					   
					   
						
    # Examples:
    # url(r'^$', 'djitter.views.home', name='home'),
    # url(r'^djitter/', include('djitter.foo.urls')),

     Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
