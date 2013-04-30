import webapp2
import jinja2
import os
import json
import random
import logging
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('gameScreen.html')
		template_values = {}
		self.response.write(template.render(template_values))

class ConnectHandler(webapp2.RequestHandler):
	def get(self):
		code = self.request.get('roomCode')
		#todo: first need to create room before implementing join


		template = JINJA_ENVIRONMENT.get_template('connect.html')
		template_values = {'code':code,}
		self.response.write(template.render(template_values))

numToLetter = ['a', 'b', 'd', 'l', 'r', 'u']

#temporary code to test controller
class ControlsTestHandler(webapp2.RequestHandler):
	def post(self):
		button_letter = self.request.get('button')
		# initialize to 'none'
		memcache.add(key='letter', value='none', time=3600)
		self.update_letter('letter', button_letter)

	def get(self):
		letter = memcache.get('letter')
		if letter is None:
			letter = 'none'

		template = JINJA_ENVIRONMENT.get_template('controlsTest.html')
		template_values = {'letter':letter,}
		self.response.write(template.render(template_values))

	def update_letter(self, key, value):
	   client = memcache.Client()
	   while True:
	     counter = client.gets(key)
	     sequence = client.gets("sequence")
	     logging.info(counter)
	     logging.info(sequence)
	     assert counter is not None, 'Uninitialized counter'
	     if client.cas(key, value):
		if counter == numToLetter[int(sequence)]:
			self.response.write(json.dumps({"status": "true"}))
		else:
			self.response.write(json.dumps({"status": "false"}))
	        break

class UpdateSequence(webapp2.RequestHandler):
	def get(self):
		num = self.request.get('num')
		memcache.add(key='sequence', value=num, time=2)

class GenerateRandomButtons(webapp2.RequestHandler):
	def get(self):
		data = {'array': []}
		for x in range(0, 200):
			data['array'].append(random.randint(0,5))
		jsonObj = json.dumps(data)
		self.response.write(jsonObj)
		memcache.add(key="sequence", value="none", time=2)

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage, name='main'),
	webapp2.Route(r'/room/connect', handler=ConnectHandler, name='connect'),
	webapp2.Route(r'/game/test/controls', handler=ControlsTestHandler, name='controls_test'),
	webapp2.Route(r'/game/test/sequence', handler=GenerateRandomButtons, name='sequence'),
	webapp2.Route(r'/game/test/update', handler=UpdateSequence, name='update')
	], debug=True)
