#!/usr/bin/env python
from google.appengine.api import users
from main.clases.Mensaje import Mensaje
from main.clases.TipoMensaje import TipoMensaje
from main.utilidades import utilGen
import simplejson as json
import webapp2
from main.utilidades.BaseHandler import BaseHandler


class GestionMensajes(BaseHandler):
    def get(self):
        if users.get_current_user() and users.is_current_user_admin():            
            query = Mensaje.all()
            arr = query.fetch(10)
            
            self.context["cols"] = 6
            self.context["arr"] = arr
            
            self.render(__file__)
        else:
            self.redirect(self.context['config']['urlRoot'])
            
    def post(self):
        idaux = -1
        accion = self.request.get('accion')
        if accion == "I":
            obj = Mensaje()
        elif accion == "A":
            idObject = int(self.request.get("id"))
            obj = Mensaje.get_by_id(idObject)
            
        obj.cod = self.request.get('cod')
        obj.msj = self.request.get('msj')
        if self.request.get('lTipo'):
            idaux = int(self.request.get('lTipo'))
            obj.lTipo = TipoMensaje.get_by_id(idaux)
        key = obj.put()
        
        newObj = obj
        if self.request.get('lTipo'):
            newObj.lTipo.id = idaux
        newObj.id = key.id()

        self.response.out.write(json.dumps({ "obj" : utilGen.to_dict(newObj), "msj" : 1 }))
        
class ConsMensajes(webapp2.RequestHandler):
    def get(self):
        query = Mensaje.all()
        arr = query.fetch(10000)

        output = {}

        for obj in arr:
            output[obj.key().id()] = utilGen.to_dict(obj)
        
        self.response.out.write(json.dumps(output))