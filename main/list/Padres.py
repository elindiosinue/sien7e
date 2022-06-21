#!/usr/bin/env python
import simplejson as json

from google.appengine.ext import webapp
from main.clases.Pantalla import Pantalla

class Padres(webapp.RequestHandler):
    def get(self):
        aprox = self.request.get('input')
        tam = self.request.get('max')
        
        query = Pantalla.all()
        arr = query.fetch(1000)
        
        
        output = {}
        
        i = 1
        for obj in arr:
            if aprox:
                if str.find(str.upper(str(obj.nombre)), str.upper(str(aprox))) != -1 and i <= tam:
                    output["obj" + str(i)] = { 
        							"id" : obj.key().id(),
        							"nombre" : obj.nombre
        							}
                    i = i + 1

        self.response.out.write(json.dumps(output))