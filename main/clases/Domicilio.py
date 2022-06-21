'''
Created on 23/10/2011

@author: magui
'''
from google.appengine.ext import db
from Cliente import Cliente

class Domicilio(db.Model):
    idCliente = db.ReferenceProperty(Cliente)
    telefono = db.IntegerProperty
    fax = db.IntegerProperty
    email = db.EmailProperty
    direccion = db.StringProperty
    ppal = db.BooleanProperty