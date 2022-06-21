#!/usr/bin/env python
from apiclient.discovery import build
from handlers.BaseHandler import *
from oauth2client.appengine import oauth2decorator_from_clientsecrets
import httplib2
import os
from google.appengine.api import users
import simplejson as json
import string
import webapp2

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

class Login(BaseHandler):
    @decorator.oauth_required
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(string.replace(self.request.path,'/login/','/mensajes/?codmsj=2'))
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(string.replace(self.request.path,'/login/','/mensajes/?codmsj=1'))
            url_linktext = 'Login'

        self.response.out.write(json.dumps({ "url": url, "url_linktext": url_linktext }))
