from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Template, Context

from djweet.models import *

# If the user is logged in, the homepage shows the 25 most recent chirps.
# Otherwise, show the welcome page.
def index(req):
	if req.user.is_authenticated():
		user = User.objects.get(id=UID)
		chirps = Chirp.objects.filter(user__id__in = user.following).order_by('date_added')[:25]
		return render_to_response("index.html", {'username': user.username,
												 'chirps': chirps,
												 'following': user.following,},
												 context_instance = RequestContext(req))
	else:
		return render_to_response("welcome.html", context_instance = RequestContext(req))


# View a user's profile.
def view_profile(req, user):
	if req.path[-1] == '/':
		return redirect(req.path[:-1])

	user = User.objects.get(username=user)
	chirps = user.chirp_set.all()
	return render_to_response('ViewProfile.html', { 'username': user.username,
													'profile': user.profile,
													'mine': (user == req.user),
													'chirps': chirps, 
													'following': user.profile.following.all(),
													'followers': user.follower_set.all()},
													context_instance = RequestContext(req))
								

# Edit your profile.
def edit_profile(req):
	if req.method == 'POST':
		form = ProfileForm(req.POST, instance=Profile.objects.get(user=req.user))
		if form.is_valid():
			form.save()
			return redirect(reverse('profile', user=req.user))
	else:
		form = ProfileForm()
	return render_to_response('EditProfile.html', {'form':form}, context_instance=RequestContext(req))

# Publish a chirp.
def publish_chirp(req):
	if req.method == 'POST':
		chirp = Chirp(user = req.user, text = req['text'])
		chirp.save()

# Follow a user. No checks against following yourself;
# Users have the choice of whether to see their own chirps in the feed.
def follow_user(req, user):
	if req.method == "POST":
		req.user.following.add(User.objects.get(username=UID))

# Unfollow a user.
def unfollow_user(req, user):
	if req.method == "POST":
		req.user.following.remove(User.objects.get(usernam=UID))
