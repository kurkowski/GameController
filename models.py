from google.appengine.ext import ndb


#class User(ndb.Model):
#	email = ndb.StringProperty(indexed=False)
#	status = ndb.IntegerProperty(indexed=False)
#	session_key = ndb.IntegerProperty(indexed=False)

#class Friend(ndb.Model):
#	user_key1 = ndb.IntegerProperty(indexed=False)
#	user_key2 = ndb.IntegerProperty(indexed=False)

#class Game(ndb.Model):
#    game_played = ndb.IntegerProperty(indexed=False)
#    winner = ndb.IntegerProperty(indexed=False)
#    session_key = ndb.IntegerProperty(indexed=False)

class Room(ndb.Model):
	creator = ndb.StringProperty(indexed=False)
	status = ndb.IntegerProperty(indexed=False)
	limit = ndb.IntegerProperty(indexed=False)
	players = ndb.StringProperty(indexed=False, repeated=True)
	date = ndb.DateTimeProperty(auto_now_add=True)
    
	@classmethod
	def query_room(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key).order(-cls.date)

class Player(ndb.Model):
	in_room = ndb.BooleanProperty(indexed=False, default=False)
	room_owner = ndb.StringProperty(indexed=False)

	@classmethod
	def query_player(cls, ancestor_key):
		return cls.query(ancestor=ancestor_key)