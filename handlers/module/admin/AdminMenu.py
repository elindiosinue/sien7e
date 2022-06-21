#!/usr/bin/env python
import model
import simplejson as json

from main.utilidades import utilGen
from handlers.BaseHandler import BaseHandler

class AdminMenu(BaseHandler):
    def execute(self):
        method = self.request.method
        user = self.values['user']
        self.values['tab'] = '/admin'
        
        if not user or user.rol != 'admin':
            self.forbidden()
            return
        if method == 'GET':
            query = model.Pantalla.all()
            query.order("orden")
            arr = query.fetch(10000)
            if self.request.get('cons'):
                output = {}
                for obj in arr:
                    output[obj.key().id()] = utilGen.to_dict(obj)
                self.response.out.write(json.dumps(output))
            else:
                output = []
                for obj in arr:
                    output.append(utilGen.to_dict(obj))
                
                self.values["cols"] = 7
                self.values["arr"] = output
                
                self.render("templates/module/admin/admin-menu.html")
        elif method == 'POST':
            idaux = -1
            accion = self.request.get('accion')
            if accion == "I":
                obj = model.Pantalla()
            elif accion == "A":
                idObject = int(self.request.get("id"))
                obj = model.Pantalla.get_by_id(idObject)
            obj.nombre = self.request.get('nombre')
            obj.titulo = self.request.get('titulo')
            obj.url = self.request.get('url')
            obj.orden = int(self.request.get('orden'))
            if self.request.get('padre'):
                idaux = int(self.request.get('padre'))
                obj.padre = model.Pantalla.get_by_id(idaux)
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
