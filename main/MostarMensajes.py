#!/usr/bin/env python
from google.appengine.ext.webapp import template
from main.utilidades import utilGen
import webapp2


class MostarMensajes(webapp2.RequestHandler):
    def get(self):
        msj = '';
        codigo = self.request.get('codmsj');
        
        if codigo == '1':
            msj += 'Ha accedido correctamente.'
        elif codigo == '2':
            msj += 'Ha salido correctamente'
        else:
            msj += 'Los datos se han guardado correctamente.'
        
        template_values = {
                           'msj': msj,
                           }
        
        self.response.out.write(template.render(utilGen.urlPlatilla(__file__), template_values))