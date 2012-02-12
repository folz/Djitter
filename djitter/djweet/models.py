from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Profile(models.Model):
	""" A Profile keeps track of a User's information """
	
	user = models.ForeignKey(User, unique=True)
	
	name = models.CharField(max_length=30, blank=True, default="")
	
	date_added = models.DateField(auto_now_add=True)
	
	following = models.ManyToManyField(User, related_name = "follower")
	
	def __unicode__(self):
		return self.name

# Automatically create a Profile for a User if the User doesn't have one.
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Chirp(models.Model):
	""" A Chirp is a status update from a User """
	
	user = models.ForeignKey(User, unique=True)
	
	text = models.CharField(max_length=140, blank=True, default="")
	
	date_added = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return str(self.user) + str(self.date_added)


# Not necessary, but useful in demonstrating manager models
class FollowManager(models.Model):
	
	follower = models.ForeignKey(Profile)
	
	followee = models.ForeignKey(User)
	
	date_added = models.DateField(auto_now_add=True)
	

# Makes use of Django's ModelForm to autogenerate a form for the profile.
class ProfileForm(ModelForm):
	
	class Meta:
		model = Profile
		exclude = ('user')
