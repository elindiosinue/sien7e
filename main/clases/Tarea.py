from google.appengine.ext import db
from Proyecto import Proyecto

class Tarea(db.Model):
    codigo = db.StringProperty
    desc = db.StringProperty
    idProy = db.ReferenceProperty(Proyecto)
    nota = db.StringProperty(multiline=True)
    inicio = db.TimeProperty
    fin = db.TimeProperty
    hora = db.IntegerProperty
    gasto = db.IntegerProperty