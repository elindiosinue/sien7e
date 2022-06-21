from google.appengine.ext import db

class Pantalla(db.Model):
	nombre = db.StringProperty()
	titulo = db.StringProperty()
	url = db.StringProperty()
	orden = db.IntegerProperty()
	padre = db.SelfReferenceProperty()
	visible = db.BooleanProperty()
	admin = db.BooleanProperty()
