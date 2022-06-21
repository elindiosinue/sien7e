#!/usr/bin/python
from google.appengine.api import users, memcache
from oauth2client.client import AccessTokenRefreshError
from main.utilidades import utilGen
from main.utilidades.BaseHandler import BaseHandler
from datetime import datetime
import simplejson as json
from apiclient.discovery import build
import os
import httplib2
from oauth2client.appengine import oauth2decorator_from_clientsecrets
import time
import calendar
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

class HojaTrabajo(BaseHandler):
    @decorator.oauth_required
    def get(self):
        self.execute()
        self.render(__file__)
    
    @decorator.oauth_required
    def post(self):
        try:
            self.execute()
            #===================================================================
            # self.response.out.write(json.dumps({ "hoja" : self.context["hoja"],
            #                                      "tareas" : self.context["tareas"],
            #                                      "totalEventos" : self.context["totalEventos"],
            #                                      "totalDias" : self.context["totalDias"],
            #                                      "primerDia" : self.context["primerDia"],
            #                                      "nDias" : self.context["nDias"],
            #                                      "msj" : 1 }))
            #===================================================================
            self.render(__file__, 2)
        except AccessTokenRefreshError:
            self.redirect("/nucleo/")

    def execute(self):
        self.context["cols"] = 7
        
        mes = time.strftime("%m")
        if self.request.get("mes"):
            mes = self.request.get("mes")
            
        anio = time.strftime("%Y")
        if self.request.get("anio"):
            anio = self.request.get("anio")
        
        anioSig = anio
        mesSig = int(mes) + 1
        if mesSig < 10:
            mesSig = "0" + str(mesSig)
        elif mesSig > 12:
            mesSig = "01"
            anioSig = str(int(anio) + 1)
        else:
            mesSig = str(mesSig)
        
        meses = utilGen.meses()
        anios = utilGen.anios()
        
        datos = calendar.monthrange(int(anio), int(mes))
        
        eventos = []
        tareas = []
        totalEventos = []
        totalDias = []
        
        start_min = time.strftime("%Y-%m-%dT00:00:00.000Z", time.strptime("01" + "/" + mes + "/" + anio, "%d/%m/%Y"))
        start_max = time.strftime("%Y-%m-%dT00:00:00.000Z", time.strptime("01" + "/" + mesSig + "/" + anioSig, "%d/%m/%Y"))
        http = decorator.http()
        try:
            events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com', timeMin=start_min, timeMax=start_max).execute(http)
        except HttpError:
            events = ""
        if events != "":
            seguir = True
            while seguir:
                for event in events['items']:
                    try:
                        inicio = time.strptime(str.split(str(event["start"]["dateTime"]), "+")[0], '%Y-%m-%dT%H:%M:%S')
                        fin = time.strptime(str.split(str(event["end"]["dateTime"]), "+")[0], '%Y-%m-%dT%H:%M:%S')
                        hora = (time.mktime(fin) - time.mktime(inicio)) / 3600
                    except KeyError:
                        inicio = time.strptime(event["start"]["date"], '%Y-%m-%d')
                        fin = time.strptime(event["end"]["date"], '%Y-%m-%d')
                        hora = 8
                    diaInicio = int(time.strftime("%d", inicio))
                    diaFin = int(time.strftime("%d", fin))
                    if time.strftime("%m", inicio) != time.strftime("%m", fin):
                        diaFin = datos[1] + 1
                    if diaInicio == diaFin:
                        diaFin= diaFin + 1
                    for i in range(diaInicio, diaFin):
                        dia = str(i)
                        if i < 10:
                            dia = "0" + dia
                        fecha = datetime.strptime(dia + time.strftime("/%m/%Y", inicio), '%d/%m/%Y')
                        fechaTime = time.strptime(dia + time.strftime("/%m/%Y", inicio), '%d/%m/%Y')
                        if datetime.isoweekday(fecha) != 6 and datetime.isoweekday(fecha) != 7:
                            evento = {
                                      "codigo" : event["summary"],
                                      "dia" : time.strftime("%d/%m/%Y", fechaTime),
                                      "hora" : str(hora)
                                      }
                            sumHora = 0
                            sumTotalEventos = 0
                            sumTotalDias = 0
                            eventoOld = {}
                            totalEvento = {}
                            totalDia = {}
                            for obj in eventos:
                                if obj["codigo"] == evento["codigo"] and obj["dia"] == evento["dia"]:
                                    sumHora = str(float(obj["hora"]) + float(evento["hora"]))
                                    eventoOld = obj
                                    
                            for obj in totalEventos:
                                if obj["codigo"] == evento["codigo"]:
                                    sumTotalEventos = float(obj["hora"]) + float(evento["hora"])
                                    totalEvento = obj
                                    
                            for obj in totalDias:
                                if obj["dia"] == evento["dia"]:
                                    sumTotalDias = float(obj["hora"]) + float(evento["hora"])
                                    totalDia = obj
                                    
                            if sumHora != 0:
                                elemento = eventos.index(eventoOld)
                                eventos[elemento]["hora"] = sumHora
                            else:
                                eventos.append(evento)
                                
                            if sumTotalEventos != 0:
                                elemento = totalEventos.index(totalEvento)
                                totalEventos[elemento]["hora"] = str(sumTotalEventos)
                            else:
                                totalEventos.append({ "codigo" : evento["codigo"], "hora" : evento["hora"] })
                                
                            if sumTotalDias != 0:
                                elemento = totalDias.index(totalDia)
                                totalDias[elemento]["hora"] = str(sumTotalDias)
                            else:
                                totalDias.append({ "dia" : evento["dia"], "hora" : evento["hora"] })
                            tarea = {
                                     "codigo" : event["summary"]
                                     }
                            if tareas.count(tarea) == 0:
                                tareas.append(tarea)
                page_token = events.get('nextPageToken')
                if page_token:
                    events = service.events().list(calendarId='0500m81f493kbajc5c0ikt4ufs@group.calendar.google.com', timeMin=start_min, timeMax=start_max, pageToken=page_token).execute(http)
                else:
                    seguir = False
        
        dias = []
        i = 1
        while i <= datos[1]:
            obj = {}
            dia = str(i)
            if i < 10:
                dia = "0" + dia
            obj["dia"] = dia + "/" + mes + "/" + anio
            obj["num"] = dia
            obj["weekend"] = "N"
            fecha = datetime.strptime(obj["dia"], '%d/%m/%Y')
            if datetime.isoweekday(fecha) == 6 or datetime.isoweekday(fecha) == 7:
                obj["weekend"] = "S"
            dias.append(obj)
            i = i + 1
        
        for evento in eventos:
            evento["hora"] = str(evento["hora"]).replace(".", ",")
        
        for evento in totalEventos:
            evento["hora"] = str(evento["hora"]).replace(".", ",")
        
        for evento in totalDias:
            evento["hora"] = str(evento["hora"]).replace(".", ",")
        
        self.context["nDias"] = str(datos[1])
        self.context["mes"] = mes
        self.context["anio"] = anio
        self.context["meses"] = meses
        self.context["anios"] = anios
        self.context["dias"] = dias
        self.context["hoja"] = eventos
        self.context["tareas"] = tareas
        self.context["totalEventos"] = totalEventos
        self.context["totalDias"] = totalDias
        self.context["primerDia"] = str(datos[0])
        self.context["nDias"] = str(datos[1])
