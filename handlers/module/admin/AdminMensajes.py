#!/usr/bin/env python
from main.clases.Mensaje import Mensaje
from main.clases.TipoMensaje import TipoMensaje
from main.utilidades import utilGen
import simplejson as json
from handlers.BaseHandler import BaseHandler


class AdminMensajes(BaseHandler):
    def execute(self):
        method = self.request.method
        user = self.values['user']
        self.values['tab'] = '/admin'
        
        if not user or user.rol != 'admin':
            self.forbidden()
            return
        if method == 'GET':
            query = Mensaje.all()
            arr = query.fetch(10000)
            if self.request.get('cons'):
                output = {}
                for obj in arr:
                    output[obj.key().id()] = utilGen.to_dict(obj)
                self.response.out.write(json.dumps(output))
            else:
                self.values["cols"] = 6
                self.values["arr"] = arr
                
                self.render("templates/module/admin/admin-mensajes.html")
        elif method == 'POST':
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