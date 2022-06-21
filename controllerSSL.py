#!/usr/bin/python
# -*- coding: utf-8 -*-

##
# (C) Copyright 2011 Jose Carrasco <jose.carrasco[a]vikuit.com>
# (C) Copyright 2011 Jose Blanco <jose.blanco[a]vikuit.com>
#
# This file is part of "vikuit".
#
# "vikuit" is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# "vikuit" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with "vikuit".  If not, see <http://www.gnu.org/licenses/>.
##

from handlers import Updater
from main import *
import webapp2
import wsgiref.handlers

# from google.appengine.ext import webapp
# from google.appengine.ext.webapp import template

# webapp.template.register_template_library('django.contrib.markup.templatetags.markup')
# webapp.template.register_template_library('templatefilters')

def main():
	Updater.update()

	application = webapp2.WSGIApplication(
									   [
									   ('/nucleo/login/.*', 						Login),
									   ('/nucleo/menu/.*', 							Menu),
									   ('/nucleo/guestbook/mensajes/.*', 			ConsMensajesGuestBook),
									   ('/nucleo/guestbook/.*', 					GuestBook),
									   ('/nucleo/grafmun/.*', 						GrafMun),
									   ('/nucleo/grafico2011/.*', 					Grafico2011),
									   ('/nucleo/grafico2008/.*', 					Grafico2008),
									   ('/nucleo/mensajes/.*', 						MostarMensajes),
									   ('/nucleo/calendar/.*', 						Calendar),
									   ('/nucleo/eventos/.*', 						GestionEventos),
									   ('/nucleo/tareas/.*', 						GestionTareas),
									   ('/nucleo/hojatrabajo/.*', 					HojaTrabajo),
									   ('/nucleo/horassindicales/.*', 				HorasSindicales),
									   ('/nucleo/admin/tiposmensajes/cons', 		ConsTiposMensajes),
									   ('/nucleo/admin/tiposmensajes/.*', 			GestionTiposMensajes),
									   ('/nucleo/admin/mensajes/cons', 				ConsMensajes),
									   ('/nucleo/admin/mensajes/.*', 				GestionMensajes),
									   ('/nucleo/admin/menu/cons', 					ConsMenu),
									   ('/nucleo/admin/menu/.*', 					GestionMenu),
									   ('/nucleo/admin/clientes/cons', 				ConsClientes),
									   ('/nucleo/admin/clientes/.*', 				GestionClientes),
									   ('/nucleo/list/padres/.*', 					Padres),
									   ('/nucleo/list/tiposmensajes/.*', 			TiposMensajes),
									   ('/nucleo/.*', 								Bienvenido), ],
									   debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()
