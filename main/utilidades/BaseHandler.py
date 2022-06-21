import webapp2
import jinja2
import os
from main.utilidades import utilGen
from main.clases.Pantalla import Pantalla
from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):

    context = {
               'env' : ''
               }

    def __init__(self, request=None, response=None):
        self.populateContext()
        self.initialize(request, response)

    def populateContext(self):
        config = {
                  'theme': 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/themes/cupertino/jquery-ui.css',
                  'urlRoot': '/nucleo/',
                  'urlRootSsl': '/nucleo/'
                  }
        volver = { "url" : config['urlRoot'],    "nombre" : "Menu" }
        self.context["url_linktext"] = "Logout"
        self.context['config'] = config
        self.context["volver"] = volver
        
    def render(self, template_name, tipo = 1):
        #self.datosPantalla(template_name)
        jinja_environment = jinja2.Environment(
                                               loader=jinja2.FileSystemLoader(os.path.dirname(utilGen.urlPlatilla(template_name, tipo))))
        template = jinja_environment.get_template(utilGen.nomPlatilla(template_name))
        self.response.out.write(template.render(self.context))
        
    def datosPantalla(self, fichPy):
        sep = "/"
        if str.find(fichPy,"\\") != -1:
            sep = "\\"
        arr = str.split(fichPy, sep)
        fich = str.split(arr[arr.__len__() - 1], ".")
        query = Pantalla.all().filter("nombre =",fich[0])
        pantalla = query.get()
        direccion = ""
        if fich[0] == "Bienvenido":
            direccion = self.context['config']['urlRootSsl'] + 'menu/'
        else:
            direccion = users.create_logout_url(self.context['config']['urlRoot'])
        titulo = "Sin t&iacute;tulo"
        volver = { "url" : self.context['config']['urlRoot'],    "nombre" : "Menu" }
        
        if pantalla:
            titulo = pantalla.titulo
            if pantalla.padre:
                if pantalla.padre.url != "":
                    volver = { "url" : pantalla.padre.url, "nombre"    : pantalla.padre.nombre    }
        else:
            if fich[0] == "Bienvenido":
                titulo = "Bienvenido"
            elif fich[0] == "Menu":
                titulo = "Menu"
        
        self.context["titulo"] = titulo
        self.context["volver"] = volver
        self.context["url"] = direccion
        self.context["url_linktext"] = "Logout"