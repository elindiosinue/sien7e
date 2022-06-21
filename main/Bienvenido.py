#!/usr/bin/python
from main.utilidades.BaseHandler import BaseHandler
from google.appengine.api import users

class Bienvenido(BaseHandler):
    def	get(self):
        env = self.request.get('env')
        self.context['env'] = env
    	user = users.get_current_user()
        if user:
            self.redirect('/nucleo/menu/')
        else:
            self.render(__file__)
            
