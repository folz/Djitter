from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField

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
	date_added = models.DateTimeField(auto_now_add=True)
	
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
		exclude = ('user', 'following')
		
class ChirpForm(ModelForm):
	text = CharField(label="Update status:")
	class Meta:
		model = Chirp
		exclude = ('user',)
