from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Profile model: basic user info and a M2MField of users they are following.
class Profile(models.Model):
	user = models.ForeignKey(User, unique=True)
	name = models.CharField(max_length=30, blank=True, default="")
	date_added = models.DateField(auto_now_add=True)
	following = models.ManyToManyField(User, related_name = "follower")
	
	def __unicode__(self):
		return self.name
# If user doesn't have a profile yet, autocreate one!
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


# Chirp model: FKey to owner, text field, and date for sorting.
class Chirp(models.Model):
	user = models.ForeignKey(User, unique=True)
	text = models.CharField(max_length=140, blank=True, default="")
	date_added = models.DateField(auto_now_add=True)
	
	def __unicode__(self):
		return self.user + self.date_added
		
		
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
