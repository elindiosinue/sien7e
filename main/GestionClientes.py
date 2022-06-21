#!/usr/bin/env python
from google.appengine.api import users
from main.clases.Cliente import Cliente
from main.utilidades import utilGen
import simplejson as json
import webapp2
from main.utilidades.BaseHandler import BaseHandler


class GestionClientes(BaseHandler):
    def get(self):
        if users.get_current_user() and users.is_current_user_admin():                
            query = Cliente.all()
            arr = query.fetch(1000)
            
            self.context["cols"] = 7
            self.context["arr"] = arr
                               
            self.render(__file__)
        else:
            self.redirect(self.context['config']['urlRoot'])
            
    def post(self):
        accion = self.request.get('accion')
        if accion == "I":
            obj = Cliente()
        elif accion == "A":
            idObject = int(self.request.get("id"))
            obj = Cliente.get_by_id(idObject)
        obj.nombre = self.request.get('nombre')
        obj.nFiscal = self.request.get('nFiscal')
        if self.request.get('nota'):
            obj.nota = self.request.get('nota')
        
        key = obj.put()
        
        newObj = obj
        newObj.id = key.id()

        self.response.out.write(json.dumps({ "obj" : utilGen.to_dict(newObj), "msj" : 1 }))
        
class ConsClientes(webapp2.RequestHandler):
    def get(self):
        query = Cliente.all()
        arr = query.fetch(10000)

        output = {}

        for obj in arr:
            output[obj.key().id()] = utilGen.to_dict(obj)
        
        self.response.out.write(json.dumps(output))