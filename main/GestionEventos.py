#!/usr/bin/python
from google.appengine.api import users, memcache
from oauth2client.client import AccessTokenRefreshError
from main.utilidades.BaseHandler import BaseHandler
import simplejson as json
from apiclient.discovery import build
import os
import httplib2
from oauth2client.appengine import oauth2decorator_from_clientsecrets
import time
from apiclient.errors import HttpError

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

class GestionEventos(BaseHandler):
    @decorator.oauth_required
    def get(self):
        self.context["cols"] = 7
        self.render(__file__)
    
    @decorator.oauth_required
    def post(self):
        start_min = ''
        if self.request.get('from') != '':
            start_min = time.strftime("%Y-%m-%dT00:00:00.000Z", time.strptime(self.request.get('from'), "%d/%m/%Y"))
        start_max = ''
        if self.request.get('to') != '':
            start_max = time.strftime("%Y-%m-%dT00:00:00.000Z", time.strptime(self.request.get('to'), "%d/%m/%Y"))
        tarea = self.request.get('tarea')
        if users.get_current_user():  
            if start_min != '' and start_max != '':
                http = decorator.http()
                eventos = []
                try:
                    events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com', timeMin=start_min, timeMax=start_max).execute(http)
                except HttpError:
                    events = ""
                if events != "":
                    seguir = True
                    while seguir:
                        for event in events['items']:
                            if tarea != '' and event["summary"] == tarea:
                                inicio = time.strptime(str.split(str(event["start"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                fin = time.strptime(str.split(str(event["end"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                hora = (time.mktime(fin) - time.mktime(inicio)) / 3600
                                evento = {
                                         "codigo" : event["summary"],
                                         "inicio" : time.strftime("%d/%m/%Y %H:%M:%S", inicio),
                                         "fin" : time.strftime("%d/%m/%Y %H:%M:%S", fin),
                                         "hora" : hora
                                         }
                                eventos.append(evento)
                            else:
                                inicio = time.strptime(str.split(str(event["start"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                fin = time.strptime(str.split(str(event["end"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                hora = (time.mktime(fin) - time.mktime(inicio)) / 3600
                                evento = {
                                         "codigo" : event["summary"],
                                         "inicio" : time.strftime("%d/%m/%Y %H:%M:%S", inicio),
                                         "fin" : time.strftime("%d/%m/%Y %H:%M:%S", fin),
                                         "hora" : hora
                                         }
                                eventos.append(evento)
                        page_token = events.get('nextPageToken')
                        if page_token:
                            events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com', timeMin=start_min, timeMax=start_max, pageToken=page_token).execute(http)
                        else:
                            seguir = False
            elif tarea != '':
                http = decorator.http()
                eventos = []
                try:
                    events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com').execute(http)
                except HttpError:
                    events = ""
                if events != "":
                    seguir = True
                    sumary = ''
                    sumHoras = 0
                    while seguir:
                        for event in events['items']:
                            if event["summary"] == tarea:
                                inicio = time.strptime(str.split(str(event["start"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                fin = time.strptime(str.split(str(event["end"]["dateTime"]),"+")[0], '%Y-%m-%dT%H:%M:%S')
                                hora = (time.mktime(fin) - time.mktime(inicio)) / 3600
                                evento = {
                                         "codigo" : event["summary"],
                                         "inicio" : time.strftime("%d/%m/%Y %H:%M:%S", inicio),
                                         "fin" : time.strftime("%d/%m/%Y %H:%M:%S", fin),
                                         "hora" : hora
                                         }
                                sumHoras = sumHoras + hora
                                sumary = event["summary"]
                                eventos.append(evento)
                        page_token = events.get('nextPageToken')
                        if page_token:
                            events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com', pageToken=page_token).execute(http)
                        else:
                            seguir = False
                    evento = {
                                "codigo" : sumary,
                                "inicio" : '',
                                "fin" : '',
                                "hora" : sumHoras
                              }
            eventos.append(evento)
        self.response.out.write(json.dumps({ "eventos" : eventos, "msj" : 1 }))
