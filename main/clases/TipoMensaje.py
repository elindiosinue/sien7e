from google.appengine.ext import db

class TipoMensaje(db.Model):
	cod = db.StringProperty()
	tipo = db.StringProperty()