## Setting up 

## Design application flow

We want to be able to do a few things:

1. View a homepage feed of all the chirps of everyone I'm following
2. View individual Djitter users' profiles
3. Edit my profile
4. Publish chirps
5. Follow other Djitter users
6. See a list of all users on site
7. Search for hashtags

## URLConf

	url(r'^$', 'chirp.views.home', name='home'),
	
	url(r'(?P<username>\w+)$', 'chirp.views.view', name='view'),
	
	url(r'edit/$', 'chirp.views.edit', name='edit'),
	
	url(r'publish/$', 'chirp.views.cheep', name='cheep'),
	
	url(r'follow/(?P<username>\w+)/$', 'chirp.views.follow', name='follow'),
	
	url(r'connect/$', 'chirp.views.connect', name='connect'),

## Edit views

`
