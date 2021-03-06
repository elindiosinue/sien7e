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

from handlers.AuthenticatedHandler import *
from google.appengine.api import users

class UserDrafts(AuthenticatedHandler):

	def execute(self):
		user = self.get_current_user()
		query = model.Article.all().filter('author =', user).filter('draft =', True).filter('deletion_date', None)
		self.values['articles'] = self.paging(query, 10, '-last_update', user.draft_articles, ['-last_update'])
		self.render('templates/module/user/user-drafts.html')
