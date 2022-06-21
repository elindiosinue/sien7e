#!/usr/bin/python
from main.clases.Pantalla import Pantalla
from google.appengine.api import users, memcache
from main.utilidades.BaseHandler import BaseHandler
import os
import httplib2
from apiclient.discovery import build
from oauth2client.appengine import oauth2decorator_from_clientsecrets
# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS


http = httplib2.Http(memcache)
service = build("calendar", "v3", http=http)
decorator = oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    'https://www.googleapis.com/auth/calendar',
    MISSING_CLIENT_SECRETS_MESSAGE)

class Menu(BaseHandler):
    @decorator.oauth_aware
    def	get(self):
        if users.get_current_user():
            query = Pantalla.all()
            query.filter("visible =", True)
            
            if not users.is_current_user_admin():
                query.filter("admin	=", False)
            query.order("orden")
            pantallas = query.fetch(10000)
            
            self.context["objs"] = pantallas
            self.render(__file__)
        else:
            self.redirect('/nucleo/')
