#!/usr/bin/env python
from main.clases.Cliente import Cliente
from main.utilidades import utilGen
import simplejson as json
from handlers.BaseHandler import BaseHandler


class AdminClientes(BaseHandler):
    def execute(self):
        method = self.request.method
        user = self.values['user']
        self.values['tab'] = '/admin'
        
        if not user or user.rol != 'admin':
            self.forbidden()
            return
        if method == 'GET':
            query = Cliente.all()
            arr = query.fetch(10000)
            if self.request.get('cons'):
                output = {}
                for obj in arr:
                    output[obj.key().id()] = utilGen.to_dict(obj)
                
                self.response.out.write(json.dumps(output))
            else:
                self.values["cols"] = 7
                self.values["arr"] = arr
                                   
                self.render("templates/module/admin/admin-clientes.html")
        elif method == 'POST':
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