from google.appengine.ext import db
from Cliente import Cliente

class Proyecto(db.Model):
	nombre = db.StringProperty
	codigo = db.StringProperty
	idCliente = db.ReferenceProperty(Cliente)
	nota = db.StringProperty(multiline=True)
	hora = db.TimeProperty
	gasto = db.IntegerProperty