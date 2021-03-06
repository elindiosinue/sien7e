#!/usr/bin/python
# -*- coding: utf-8 -*-

##
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
import model
import logging

from google.appengine.api import memcache
from google.appengine.ext import webapp
from handlers.BaseHandler import BaseHandler

class ImageBrowser(BaseHandler):
    
    def execute(self):
        user = self.values['user']
        
        #TODO PAGINATE
        if user:
            list = ""
            if user.rol == 'admin':
                images = model.Image.all()
            else:
                images = model.Image.gql('WHERE author_nickname=:1', user.nickname)
        
        self.values['images'] = images
        self.render('templates/editor/browse.html')         
        return
