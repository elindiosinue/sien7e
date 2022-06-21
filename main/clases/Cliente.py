#!/usr/bin/python
from google.appengine.ext import db

class Cliente(db.Model):
	nombre = db.StringProperty()
	nFiscal = db.StringProperty()
	nota = db.StringProperty(multiline=True)