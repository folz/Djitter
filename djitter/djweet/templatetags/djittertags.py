import urllib, hashlib
from django import template

register = template.Library()

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
		

def gravatar_url(parser, token):
	email, size = token.split_contents()[1:]	
	return GravatarNode(email, size)

gravatar_url = register.tag(gravatar_url)
