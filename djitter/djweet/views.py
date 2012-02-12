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
	
	if req.user.is_authenticated():
		is_following = user in req.user.profile.following.all()
	else:
		is_following = False
	
	
	return render_to_response('view.html',
			{ 'user': user
			, 'chirps': chirps
			, 'follow': 'Unfollow' if is_following else 'Follow'
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
def cheep(req):
	if req.method == 'POST':
		chirp = Chirp(user = req.user, text = req['text'])
		chirp.save()

@login_required
def follow(req, username):
	if req.method == "POST":
		user = User.objects.get(username=username)
		
		if user in req.user.profile.following.all():
			req.user.profile.following.remove(user)
		else:
			req.user.profile.following.add(user)
		
	return redirect('home')

def back_to_home(req):
	# Maps accounts/profile back to home (we don't use it)
	return redirect('home')
