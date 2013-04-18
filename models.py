from google.appengine.ext import ndb


class User(ndb.Model):
	email = ndb.StringProperty(indexed=False)
	status = ndb.IntegerProperty(indexed=False)
	session_key = ndb.IntegerProperty(indexed=False)

class Friend(ndb.Model):
	user_key1 = ndb.IntegerProperty(indexed=False)
	user_key2 = ndb.IntegerProperty(indexed=False)

class Game(ndb.Model):
    game_played = ndb.IntegerProperty(indexed=False)
    winner = ndb.IntegerProperty(indexed=False)
    session_key = ndb.IntegerProperty(indexed=False)

class Session(ndb.Model):
	creator = ndb.IntegerProperty(indexed=False)
	status = ndb.IntegerProperty(indexed=False)

    