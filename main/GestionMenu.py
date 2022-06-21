#!/usr/bin/env python
from google.appengine.api import users
from main.clases.Pantalla import Pantalla
from main.utilidades import utilGen
import simplejson as json
import webapp2
from main.utilidades.BaseHandler import BaseHandler


class GestionMenu(BaseHandler):
    def get(self):
        if users.get_current_user() and users.is_current_user_admin():
            query = Pantalla.all()
            query.order("orden")
            arr = query.fetch(1000)
            
            output = []
            for obj in arr:
                output.append(utilGen.to_dict(obj))
            
            self.context["cols"] = 7
            self.context["arr"] = output
            
            self.render(__file__)
        else:
            self.redirect(self.context['config']['urlRoot'])

    def post(self):
        idaux = -1
        accion = self.request.get('accion')
        if accion == "I":
            obj = Pantalla()
        elif accion == "A":
            idObject = int(self.request.get("id"))
            obj = Pantalla.get_by_id(idObject)
        obj.nombre = self.request.get('nombre')
        obj.titulo = self.request.get('titulo')
        obj.url = self.request.get('url')
        obj.orden = int(self.request.get('orden'))
        if self.request.get('padre'):
            idaux = int(self.request.get('padre'))
            obj.padre = Pantalla.get_by_id(idaux)
        if self.request.get('visible') == "true":
            obj.visible = True
        else:
            obj.visible = False
        if self.request.get('admin') == "true":
            obj.admin = True
        else:
            obj.admin = False
        key = obj.put()
        
        newObj = obj
        if self.request.get('padre'):
            newObj.padre.id = idaux
        newObj.id = key.id()

        self.response.out.write(json.dumps({ "obj" : utilGen.to_dict(newObj), "msj" : 1 }))

class ConsMenu(webapp2.RequestHandler):
    def get(self):
        query = Pantalla.all()
        arr = query.fetch(10000)

        output = {}

        for obj in arr:
            output[obj.key().id()] = utilGen.to_dict(obj)
        
        self.response.out.write(json.dumps(output))
