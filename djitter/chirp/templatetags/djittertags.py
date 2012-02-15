import urllib, hashlib, re
from django import template
from django.core.urlresolvers import reverse

register = template.Library()
		
def gravatar(email, size):
	return "http://www.gravatar.com/avatar.php?"+ urllib.urlencode({ 'gravatar_id': hashlib.md5(email).hexdigest()
																	  , 'size': str(size)
																	  })
																	  

def chirptag(parser, token):
	text = token.split_contents()[1]
	return ChirpNode(text)
	
class ChirpNode(template.Node):
	def __init__(self, text):
		self.text = template.Variable(text)
		
	def render(self, context):
		text = self.text.resolve(context)
		text = re.sub(r'@([a-zA-Z0-9_]*)', r'<a href = "'+reverse('view')+r'\1">@\1</a>', text)
		text = re.sub(r'#([a-zA-Z0-9_]*)', r'<a href = "'+reverse('discover')+r'?tags=\1">#\1</a>', text)
		return text


gravatar = register.filter(gravatar)
chirptag = register.tag(chirptag)
