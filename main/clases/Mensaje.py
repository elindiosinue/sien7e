from google.appengine.ext import db
from TipoMensaje import TipoMensaje

class Mensaje(db.Model):
	cod = db.StringProperty()
	lTipo = db.ReferenceProperty(TipoMensaje)
	msj = db.StringProperty(multiline=True)