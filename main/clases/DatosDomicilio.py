from google.appengine.ext import db
from Cliente import Cliente

class DatosDomicilio(db.Model):
	telefono = db.PhoneNumberProperty()
	fax = db.PhoneNumberProperty()
	email = db.EmailProperty()
	direccion = db.StringProperty()
	cliente = db.ReferenceProperty(Cliente)
