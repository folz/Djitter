from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Template, Context

from chirp.models import *

@login_required
def home(req):
	chirps = Chirp.objects.filter(user__in = list(req.user.profile.following.all()) + [req.user]) | req.user.mentions.all()
	chirps = chirps.order_by('-date_added')
	return render_to_response("index.html",
			{ 'chirps': chirps
			, 'chirper': ChirpForm()
			}
		, context_instance = RequestContext(req))

@login_required
def connect(req):
	users = User.objects.all()
	return render_to_response("connect.html",
			{ 'users': users
			, 'chirper': ChirpForm()
			}
		, context_instance = RequestContext(req))

def view(req, username):
	user = User.objects.get(username=username)
	chirps = (user.chirp_set.all() | user.mentions.all()).order_by('-date_added')[:25]
	
	if req.user.is_authenticated():
		is_following = user in req.user.profile.following.all()
	else:
		is_following = False
	
	return render_to_response('view.html',
			{ 'viewing': user
			, 'chirper': ChirpForm()
			, 'chirps': chirps
			, 'follow': 'Unfollow' if is_following else 'Follow'
			, 'following': is_following
			, 'mine': req.user == user
			}
		, context_instance = RequestContext(req))

@login_required
def edit(req):
	if req.method == 'POST':
		form = ProfileForm(req.POST, instance=Profile.objects.get(user=req.user))
		if form.is_valid():
			form.save()
			return redirect('view', req.user.username)
	else:
		form = ProfileForm(instance=Profile.objects.get(user=req.user))
	return render_to_response('edit.html',
			{ 'form': form
			, 'chirper': ChirpForm()
			}
		, context_instance=RequestContext(req))

@login_required
def cheep(req):
	if req.method == 'POST':
		if req.POST['text'] != "":
			chirp = Chirp(user = req.user, text = req.POST['text'])
			chirp.save()
			words = req.POST['text'].split()
			for word in words:
				if word[0] == '@':
					matched = User.objects.filter(username=word[1:])
					if matched: chirp.mentions.add(matched[0])
				elif word[0] == '#':
					chirp.topics.add(word[1:].lower())
	return redirect('home')
	
@login_required
def discover(req):
	form = SearchForm(req.GET)
	if req.method == 'GET':
		if form.is_valid():
			terms = form.cleaned_data['tags'].lower().replace(',', ' ').split()
			chirps = Chirp.objects.filter(topics__name__in = terms).distinct()
			return render_to_response('discover.html', { 'form': form
													   , 'chirps': chirps
													   }
													   , context_instance=RequestContext(req))
	return render_to_response('discover.html', { 'form': form
											   , 'chirps': []
											   }
											   , context_instance=RequestContext(req))

@login_required
def follow(req, username):
	if req.method == 'POST':
		user = User.objects.get(username=username)
		
		if user in req.user.profile.following.all():
			req.user.profile.following.remove(user)
			messages.add_message(req, messages.INFO, '''You stopped following {}.'''.format(user.username))
		else:
			req.user.profile.following.add(user)
			messages.add_message(req, messages.INFO, '''You're now following {}.'''.format(user.username))
	return redirect('view', username)

def back_to_home(req):
	# Maps accounts/profile back to home (we don't use it)
	return redirect('home')