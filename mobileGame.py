import webapp2
import jinja2
import os
import json
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.api import channel
from models import *
import random
import logging


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

numToLetter = ['a', 'b', 'd', 'l', 'r', 'u', 's']

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
		#user_nickname = getUser(self)	
		#player = Player.query_player(user_key(user_nickname)).fetch(1)
		#if player:
		#	player = player[0]
		#else:
		#player = None
		#template = JINJA_ENVIRONMENT.get_template('templates/index.html')
		#template_values = {'name':user_nickname, 'inRoom':player}
		template = JINJA_ENVIRONMENT.get_template('gameScreen.html')
		template_values = {}
		self.response.write(template.render(template_values))

class CreateHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		if player.in_room:
			self.redirect('/room')
			#redirect to his room
		else:
			room = Room(parent = user_key(user_nickname))
			room.creator = user_nickname
			room.status = 1
			room.limit = 4
			room.players = []
			player.in_room = True
			player.room_owner = user_nickname
			room.put()
			player.put()
			template = JINJA_ENVIRONMENT.get_template('templates/create.html')
			template_values = {'creator':room.creator, 'date':room.date, 'players':room.players, 'inRoom':player.in_room}
			self.response.write(template.render(template_values))

class ConnectHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		creator_nickname = self.request.get('creatorNickname')

		if player.in_room:
			self.redirect('/room')
			#redirect to his room

		room = Room.query_room(user_key(creator_nickname)).fetch(1)
		if room:
			room = room[0]
			status = room.status
			date = room.date
			room.players.append(user_nickname)
			players = room.players
			player.in_room = True
			player.room_owner = creator_nickname
			room.put()
			player.put()
		else:
			#fix: print error message
			status = -1
			date = -1
			players = []

		template = JINJA_ENVIRONMENT.get_template('templates/connect.html')
		template_values = {'creatorNickname':creator_nickname, 
							'status':status, 
							'date': date, 
							'players': players,}
		self.response.write(template.render(template_values))

class RoomHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		room = Room.query_room(user_key(player.room_owner)).fetch(1)[0]
		if room:
			creator_nickname = room.creator
			status = room.status
			date = room.date
			players = room.players

			token = channel.create_channel(user_nickname + player.room_owner)



			template = JINJA_ENVIRONMENT.get_template('templates/room.html')
			template_values = {'creator':creator_nickname, 
								'status':status, 
								'date': date, 
								'players': players,
								'player':player,
								'token':token, }
			self.response.write(template.render(template_values))
		else:
			self.redirect('/')

class MonitorHandler(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		if player.in_room:
			room = Room.query_room(user_key(player.room_owner)).fetch(1)[0]
			room.monitor = user_nickname
			room.put()

			creator_nickname = room.creator
			status = room.status
			date = room.date
			players = room.players

			token = channel.create_channel(player.room_owner)
			template = JINJA_ENVIRONMENT.get_template('templates/room.html')
			template_values = {'creator':creator_nickname, 
								'status':status, 
								'date': date, 
								'players': players,
								'player':player,
								'token':token, }
			self.response.write(template.render(template_values))

		else:
			self.redirect('/home')


class PlayHandler(webapp2.RequestHandler):
	def get(self):

		user_nickname = getUser(self)	
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]

		creator = player.room_owner
		room = Room.query_room(user_key(creator)).fetch(1)[0]
		player_nickname = room.players[0]

		logging.info("here")

		channel.send_message(creator, json.dumps({'message':'monitor'}))
		channel.send_message(player_nickname+creator, json.dumps({'message':'controller'}))
		logging.info("here")


class PlayMonitor(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)	
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]

		creator = player.room_owner
		room = Room.query_room(user_key(creator)).fetch(1)[0]
		player_nickname = room.players[0]

		token = channel.create_channel(player.room_owner)
		template = JINJA_ENVIRONMENT.get_template('templates/gameScreen.html')
		template_values = {'token':token, }
		self.response.write(template.render(template_values))



class PlayController(webapp2.RequestHandler):
	def get(self):
		user_nickname = getUser(self)	
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]

		creator = player.room_owner
		room = Room.query_room(user_key(creator)).fetch(1)[0]
		player_nickname = room.players[0]

		token = channel.create_channel(user_nickname + player.room_owner)
		template = JINJA_ENVIRONMENT.get_template('templates/standardController.html')
		template_values = {'token':token, }
		self.response.write(template.render(template_values))


#temporary code to test controller
class ControlsTestHandler(webapp2.RequestHandler):
	def post(self):
		#user_nickname = getUser(self)	
		#player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		button_letter = self.request.get('button')
		# initialize to 'none'
		self.test_if_correct(button_letter)


	def get(self):
		letter = memcache.get('letter')
		if letter is None:
			letter = 'none'

		template = JINJA_ENVIRONMENT.get_template('templates/controlsTest.html')
		template_values = {'letter':letter,}
		self.response.write(template.render(template_values))

	def test_if_correct(self, value):
	     	sequence = memcache.get('sequence')
		if value == numToLetter[int(sequence)]:
			self.response.write(json.dumps({"stat": "true"}))
		else:
			self.response.write(json.dumps({"stat": "false"}))

class UpdateSequence(webapp2.RequestHandler):
	def get(self):
		num = self.request.get('num')
		logging.info(num);
		logging.info("update")
		memcache.set('sequence', num)
		self.response.write(json.dumps({'sequence': num}))

class GenerateRandomButtons(webapp2.RequestHandler):
	def get(self):
		data = {'array': []}
		for x in range(0, 200):
			data['array'].append(random.randint(0,6))
		jsonObj = json.dumps(data)
		memcache.add(key='sequence', value=data['array'][0])
		self.response.write(jsonObj)
		#template = JINJA_ENVIRONMENT.get_template('gameScreen.html')
		#template_values = {'letter':letter,}
		#self.response.write(template.render(template_values))
		

class Controls(webapp2.RequestHandler):
	def post(self):
		user_nickname = getUser(self)	
		player = Player.query_player(user_key(user_nickname)).fetch(1)[0]
		button_letter = self.request.get('button')
		# initialize to 'none'
		#channel.send_message(player.room_owner, json.dumps({'button':button_letter}))

	def get(self):
		letter = memcache.get('letter')
		if letter is None:
			letter = 'none'

		template = JINJA_ENVIRONMENT.get_template('templates/controlsTest.html')
		template_values = {'letter':letter,}
		self.response.write(template.render(template_values))

	def test_if_correct(self, value):
	     	sequence = memcache.get('sequence')
		if value == numToLetter[int(sequence)]:	
			self.response.write(json.dumps({"stat": "true"}))
		else:	
			self.response.write(json.dumps({"stat": "false"}))

class RunTestSuite(webapp2.RequestHandler):
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('qunitTestSuite.html')
		template_values = {}
		self.response.write(template.render(template_values))
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('qunitTestSuite.html')
		template_values = {}
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage, name='main'),	
	webapp2.Route(r'/room', handler=RoomHandler, name='room'),
	webapp2.Route(r'/room/create', handler=CreateHandler, name='create'),
	webapp2.Route(r'/room/connect', handler=ConnectHandler, name='connect'),
	webapp2.Route(r'/room/connect/Monitor', handler=MonitorHandler, name='monitor'),
	webapp2.Route(r'/room/play', handler=PlayHandler, name='play'),
	webapp2.Route(r'/room/play/monitor', handler=PlayMonitor, name='play_monitor'),
	webapp2.Route(r'/room/play/controller', handler=PlayController, name='play_controller'),
	webapp2.Route(r'/room/play/controls', handler=Controls, name='controls'),
	webapp2.Route(r'/game/test/controls', handler=ControlsTestHandler, name='controls_test'),
	webapp2.Route(r'/game/test/sequence', handler=GenerateRandomButtons, name='sequence'),
	webapp2.Route(r'/game/test/update', handler=UpdateSequence, name='update'),
	webapp2.Route(r'/testsuite', handler=RunTestSuite, name='test_suite')
	], debug=True)
