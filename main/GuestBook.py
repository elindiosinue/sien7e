#!/usr/bin/env python
#
# Copyright	2007 Google	Inc.
#
# Licensed under the Apache	License, Version 2.0 (the "License");
# you may not use this file	except in compliance with the License.
# You may obtain a copy	of the License at
#
#	  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable	law	or agreed to in	writing, software
# distributed under	the	License	is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR	CONDITIONS OF ANY KIND,	either express or implied.
# See the License for the specific language	governing permissions and
# limitations under	the	License.
#
from datetime import datetime
from google.appengine.api import users
from main.clases.Comentario import Comentario
from main.utilidades import utilGen
import simplejson as json
import webapp2
from main.utilidades.BaseHandler import BaseHandler


class GuestBook(BaseHandler):
	def	get(self):
		if users.get_current_user():			
			comentarios_query =	Comentario.all().order('-date')
			comentarios_query.filter("author =", users.get_current_user())
			comentarios	= comentarios_query.fetch(10000)
			for	comentario in comentarios:
				comentario.desde = utilGen.tiempo(comentario.date)
				
			self.context["cols"] =	6
			self.context["comentarios"] = comentarios
			
			self.render(__file__)
		else:
			self.redirect(self.context['config']['urlRoot'])
	def	post(self):
		comentarios_query =	Comentario.all().filter("titdate =", datetime.today().strftime("%d/%m/%Y"))
		comentarioAnt =	comentarios_query.get()
		
		comentario = Comentario()
		
		if comentarioAnt:
			comentarioAnt.titdate =	''
			comentarioAnt.put()
		
		comentario.titdate = datetime.today().strftime("%d/%m/%Y")
		if users.get_current_user():
			comentario.author =	users.get_current_user()
		
		comentario.content = self.request.get('content')
		comentario.put()
		self.redirect(self.context['config']['urlRootSsl'] + 'guestbook/')

class ConsMensajesGuestBook(webapp2.RequestHandler):
	def	get(self):
		comentarios_query =	Comentario.all().order('-date')
		comentarios_query.filter("author =", users.get_current_user())
		comentarios	= comentarios_query.fetch(10000)

		output = {}
		for	comentario in comentarios:
			comentario.desde = utilGen.tiempo(comentario.date)
			output[comentario.key().id()] =	utilGen.to_dict(comentario)

		self.response.out.write(json.dumps(output))