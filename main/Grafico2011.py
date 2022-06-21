from google.appengine.api import users
from main.utilidades.BaseHandler import BaseHandler



class Grafico2011(BaseHandler):
    def get(self):
        if users.get_current_user():
            self.render(__file__)
        else:
            self.redirect(self.context['config']['urlRoot'])