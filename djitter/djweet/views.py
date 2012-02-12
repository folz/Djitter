from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Template, Context

from djweet.models import *

@login_required
def home(req):
	chirps = Chirp.objects.filter(user__id__in = req.user.profile.following.all).order_by('date_added')[:25]
	return render_to_response("index.html",
			{ 'chirps': chirps
			}
		, context_instance = RequestContext(req))

def view(req, username):
	user = User.objects.get(username=username)
	chirps = Chirp.objects.filter(user=user)
	return render_to_response('view.html',
			{ 'user': user
			, 'chirps': chirps
			}
		, context_instance = RequestContext(req))

@login_required
def edit(req):
	if req.method == 'POST':
		form = ProfileForm(req.POST, instance=Profile.objects.get(user=req.user))
		if form.is_valid():
			form.save()
			return redirect(reverse('view', user=req.user))
	else:
		form = ProfileForm()
	return render_to_response('EditProfile.html', {'form':form}, context_instance=RequestContext(req))

@login_required
def publish_chirp(req):
	if req.method == 'POST':
		chirp = Chirp(user = req.user, text = req['text'])
		chirp.save()

@login_required
def follow_user(req, user):
	if req.method == "POST":
		req.user.following.add(User.objects.get(username=UID))

@login_required
def unfollow_user(req, user):
	if req.method == "POST":
		req.user.following.remove(User.objects.get(usernam=UID))

def back_to_home(req):
	# Maps accounts/profile back to home (we don't use it)
	return redirect('home')
