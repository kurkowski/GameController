import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		template_values = {}
		self.response.write(template.render(template_values))

class ConnectHandler(webapp2.RequestHandler):
	def get(self):
		code = self.request.get('roomCode')
		#todo: first need to create room before implementing join


		template = JINJA_ENVIRONMENT.get_template('connect.html')
		template_values = {'code':code,}
		self.response.write(template.render(template_values))


#temporary code to test controller
class ControlsTestHandler(webapp2.RequestHandler):
	def post(self):
		button_letter = self.request.post('button')
		# initialize to 'none'
		memcache.add(key='letter', value='none', time=3600)
		update_letter('letter', button_letter)

	def get(self):
		letter = memcache.get('letter')
		if letter is None:
			letter = 'none'

		template = JINJA_ENVIRONMENT.get_template('controlsTest.html')
		template_values = {'letter':letter,}
		self.response.write(template.render(template_values))


	def update_letter(key, value):
	   client = memcache.Client()
	   while True:
	     counter = client.gets(key)
	     assert counter is not None, 'Uninitialized counter'
	     if client.cas(key, value):
	        break


app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage, name='main'),
	webapp2.Route(r'/room/connect', handler=ConnectHandler, name='connect'),
	webapp2.Route(r'/game/test/controls', handler=ControlsTestHandler, name='controls_test'),
], debug=True)