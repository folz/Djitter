from django.http import HttpResponse, HttpResponseRedirect
from models import *
from django.shortcuts import render_to_response
from django.template import RequestContext, Template, Context

# If the user is logged in, the homepage shows the 25 most recent chirps.
# Otherwise, show the welcome page.
def Index(request):
	if request.user.is_authenticated():
		user = User.objects.get(id=UID)
		chirps = Chirp.objects.filter(user__id__in = user.following).order_by('date_added')[:25]
		return render_to_response("index.html", {'username': user.username,
												 'chirps': chirps,
												 'following': user.following,},
												 context_instance = RequestContext(request))
	else:
		return render_to_response("welcome.html", context_instance = RequestContext(request))


# View a user's profile.
def ViewProfile(request, UID):
	user = User.objects.get(id=UID)
	chirps = user.chirp_set.all()
	return render_to_response('ViewProfile.html', { 'username': user.username,
													'profile': user.profile,
													'mine': (user == request.user),
													'chirps': chirps, 
													'following': user.profile.following.all(),
													'followers': user.follower_set.all()},
													context_instance = RequestContext(request))
								

# Edit your profile.
def EditProfile(request):
	if request.method == 'POST':
        form = ProfileForm(request.POST, instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/'+str(request.user.id))
    else:
        form = ProfileForm()
    return render_to_response('EditProfile.html', {'form':form}, context_instance=RequestContext(request))
    

# Publish a chirp.
def PublishChirp(request):
	if request.method == 'POST':
		chirp = Chirp(user = request.user, text = request['text'])
		chirp.save()
		
		
# Follow a user. No checks against following yourself;
# Users have the choice of whether to see their own chirps in the feed.
def FollowUser(request, UID):
	if request.method == "POST":
		request.user.following.add(User.objects.get(id=UID))
		

# Unfollow a user.
def UnfollowUser(request, UID):
	if request.method == "POST":
		request.user.following.remove(User.objects.get(id=UID))
		
