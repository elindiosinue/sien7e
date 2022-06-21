#!/usr/bin/env python
import simplejson as json

from google.appengine.ext import webapp
from main.clases.TipoMensaje import TipoMensaje

class TiposMensajes(webapp.RequestHandler):
    def get(self):
        aprox = self.request.get('input')
        tam = self.request.get('max')
        
        query = TipoMensaje.all()
        arr = query.fetch(1000)
        
        
        output = {}
        
        i = 1
        for obj in arr:
            if aprox:
                if str.find(str.upper(str(obj.tipo)), str.upper(str(aprox))) != -1 and i <= tam:
                    output["obj" + str(i)] = { 
        							"id" : obj.key().id(),
        							"nombre" : obj.cod
        							}
                    i = i + 1

        self.response.out.write(json.dumps(output))