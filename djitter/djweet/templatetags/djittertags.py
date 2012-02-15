import urllib, hashlib, re
from django import template
from django.core.urlresolvers import reverse
from djweet.views import *

register = template.Library()

def gravatar(parser, token):
	email, size = token.split_contents()[1:]	
	return GravatarNode(email, size)

class GravatarNode(template.Node):
	def __init__(self, email, size):
		self.email = template.Variable(email)
		self.size = size
		
	def render(self, context):
		email = self.email.resolve(context)
		url = "http://www.gravatar.com/avatar.php?"+ urllib.urlencode({ 'gravatar_id': hashlib.md5(email).hexdigest()
																	  , 'size': str(self.size)
																	  })
		return url


def chirptag(parser, token):
	text = token.split_contents()[1]
	return ChirpNode(text)
	
class ChirpNode(template.Node):
	def __init__(self, text):
		self.text = template.Variable(text)
		
	def render(self, context):
		text = self.text.resolve(context)
		text = re.sub(r'@([a-zA-Z0-9_]*)', r'<a href = "{% url view \1 %}">@\1</a>', text)
		text = re.sub(r'#([a-zA-Z0-9_]*)', r'<a href = "{% url discover %}?query=\1">#\1</a>', text)
		return text


chirptag = register.tag(chirptag)
gravatar = register.tag(gravatar)
