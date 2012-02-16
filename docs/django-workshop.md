## Setting up 

## Design application flow

We want to be able to do a few things:

1. View a homepage feed of all the chirps of everyone I'm following
2. View individual Djitter users' profiles
3. Edit our profile
4. Publish chirps
5. Follow other Djitter users
6. See a list of all users on site

## Url patterns

	url(r'^$', 'chirp.views.home', name='home'),
	
	url(r'(?P<username>\w+)$', 'chirp.views.view', name='view'),
	
	url(r'edit/$', 'chirp.views.edit', name='edit'),
	
	url(r'publish/$', 'chirp.views.cheep', name='cheep'),
	
	url(r'follow/(?P<username>\w+)/$', 'chirp.views.follow', name='follow'),
	
	url(r'connect/$', 'chirp.views.connect', name='connect'),
	
	url(r'discover/$', 'chirp.views.discover', name='discover'),

## Models!

Basic models defining a User's profile and a Chirp

	from django.db import models
	from django.contrib.auth.models import User
	
	class Profile(models.Model):
		""" A Profile keeps track of a User's information """
	
		user = models.ForeignKey(User, unique=True)
		name = models.CharField(max_length=30, blank=True, default="")
		bio = models.TextField(max_length=200, blank=True, default="")
		location = models.CharField(max_length=30, blank=True, default="")
		url = models.CharField(max_length=100, blank=True, default="")
		date_added = models.DateField(auto_now_add=True)
		following = models.ManyToManyField(User, related_name = "followers")
	
		def __unicode__(self):
			return self.name
	
	# Automatically create a Profile for a User if the User doesn't have one.
	User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

	class Chirp(models.Model):
		""" A Chirp is a status update from a User """
		user = models.ForeignKey(User)
		text = models.CharField(max_length=140, blank=False, default="")
		mentions = models.ManyToManyField(User, related_name = "mentions")
		topics = TaggableManager()
		date_added = models.DateTimeField(auto_now_add=True)
	
		def __unicode__(self):
			return str(self.user) + str(self.date_added)

We can play with these models in the Django shell. In your terminal, run

`(venv)$ python djitter/manage.py shell`

If you've ever used the python interpreter, that's exactly what this is. The only difference is that manage.py sets some environment variables that makes it easier to import things from your Django project.

`>>> from djitter.chirp import models`

... make some chirps in shell ...
... be sure to .save()! ...

You can call these exact same functions in your views.py, and that's basically how you build dynamic web applications with Django.

## Views!

We have a couple of chirps we made earlier in the shell. Let's display them in a news feed.

	from django.contrib.auth.decorators import login_required
	
	@login_required
	def home(req):
		chirps = Chirp.objects.filter(user=req.user).order_by('-date_added')

All @login_required does is makes the user have to have logged in to call the request. Nothing too fancy.

Now how do we return the chirps as text to the browser? We could do something like

		ret = "<ul>"
		for chirp in chirps:
			ret += "<li>"+chirp.text+"</li>"
		ret += "</ul>"
		return ret

But that gets really cumbersome really quickly, and that doesn't even return a proper HTML page. Wouldn't it be nice if we could define some sort of template that looks just like proper HTML, but can change based on data we pass to it?

	from django.shortcuts import render\_to\_response

		return render_to_response("index.html",
				{ 'chirps': chirps
				}
			, context_instance = RequestContext(req))

Let's go over what this means. Open templates/base.html *Go over what it means*

Now that we understand what templates are, let's write one.




