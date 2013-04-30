import webapp2
import jinja2
import os
import json
from google.appengine.api import users
from google.appengine.api import memcache
from models import *

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def getUser(self):
	user = users.get_current_user()
	if user:
		player = Player.query_player(user_key(user.nickname())).fetch(1)
		if not player:
			player = Player(parent=user_key(user.nickname()))
			player.put()
		return user.nickname()
	else:
		self.redirect(users.create_login_url(self.request.uri))

def user_key(user_nickname):
	return ndb.Key('User',user_nickname or 'NotLoggedIn')


class MainPage(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)	
		player = Player.query_player(user_key(user_nickname)).fetch(1)
		template = JINJA_ENVIRONMENT.get_template('templates/index.html')
		template_values = {'name':user_nickname, 'inRoom':player}
		self.response.write(template.render(template_values))

class CreateHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		room = Room(parent = user_key(user_nickname))
		room.creator = user_nickname
		room.status = 1
		room.players = [user_nickname]
		player.in_room = True
		room.put()
		template = JINJA_ENVIRONMENT.get_template('templates/create.html')
		template_values = {'creator':room.creator, 'date':room.date, 'players':room.players, 'inRoom':player.in_room}
		self.response.write(template.render(template_values))

class ConnectHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname))
		creator_nickname = self.request.get('creatorNickname')

		room = Room.query_room(user_key(creator_nickname)).fetch(1)[0]
		if room:
			if player.in_room:
				pass
				#connect to room he is in
			else:
				room = room[0]
				status = room.status
				date = room.date
				room.players.append(user_nickname)
				players = room.players
				player.in_room = True
				player.room_owner = creator_nickname
				room.put()
		else:
			status = -1
			date = -1
			players = []

		template = JINJA_ENVIRONMENT.get_template('templates/connect.html')
		template_values = {'creatorNickname':creator_nickname, 
							'status':status, 
							'date': date, 
							'players': players,}
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

		template = JINJA_ENVIRONMENT.get_template('templates/controlsTest.html')
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
	webapp2.Route(r'/room/create', handler=CreateHandler, name='create'),
	webapp2.Route(r'/room/connect', handler=ConnectHandler, name='connect'),
	webapp2.Route(r'/game/test/controls', handler=ControlsTestHandler, name='controls_test'),
], debug=True)