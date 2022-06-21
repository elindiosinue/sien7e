from google.appengine.ext import db

class Comentario(db.Model):
	author = db.UserProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	titdate = db.StringProperty()
	desde = db.StringProperty()