#!/usr/bin/env python
from main.clases.TipoMensaje import TipoMensaje
from main.utilidades import utilGen
import simplejson as json
from handlers.BaseHandler import BaseHandler


class AdminTiposMensajes(BaseHandler):
    def execute (self):
        method = self.request.method
        user = self.values['user']
        self.values['tab'] = '/admin'
        
        if not user or user.rol != 'admin':
            self.forbidden()
            return
        
        if method == 'GET':
            query = TipoMensaje.all()
            arr = query.fetch(10000)
            if self.request.get('cons'):
                output = {}
                for obj in arr:
                    output[obj.key().id()] = utilGen.to_dict(obj)
                self.response.out.write(json.dumps(output))
            else:
                self.values["cols"] = 2
                self.values["arr"] = arr
                self.render("templates/module/admin/admin-tiposmensajes.html")
        elif method == 'POST':
            accion = self.request.get('accion')
            if accion == "I":
                obj = TipoMensaje()
            elif accion == "A":
                idObject = int(self.request.get("id"))
                obj = TipoMensaje.get_by_id(idObject)
                
            obj.cod = self.request.get('cod')
            obj.tipo = self.request.get('tipo')
            
            key = obj.put()
            
            newObj = obj
            newObj.id = key.id()
    
            self.response.out.write(json.dumps({ "obj" : utilGen.to_dict(newObj), "msj" : 1 }))