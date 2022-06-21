import time
import os

from google.appengine.api import users
from google.appengine.ext import db
from datetime import datetime

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def to_dict(model):
    output = {}
    
    if isinstance(model, db.Model):
        output["id"] = model.key().id()       
    
    for key, prop in model.properties().iteritems():
        value = getattr(model, key)
        
        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, db.GqlQuery):
            output[key] = list(value)
        elif isinstance(value, datetime):
            output2 = {}
            fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second', 'year']
            methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday']
            for field in fields:
                output2[field] = getattr(value, field)
            for method in methods:
                output2[method] = getattr(value, method)()
            output2['epoch'] = time.mktime(value.timetuple())
            output[key] = output2
        elif isinstance(value, time.struct_time):
            output[key] = list(value)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        elif isinstance(value, db.Email):
            output[key] = to_dict(value)
        elif isinstance(value, db.IM):
            output[key] = to_dict(value)
        elif isinstance(value, users.User):
            output2 = {}
            methods = ['nickname', 'email', 'auth_domain']
            for method in methods:
                output2[method] = getattr(value, method)()
            output[key] = output2
        else:
            raise ValueError('cannot encode ' + repr(prop))
    
    return output

def urlPlatilla(fichPy):
    sep = "/"
    if str.find(fichPy,"\\") != -1:
        sep = "\\"
    arr = str.split(fichPy, sep)
    fich = str.split(arr[arr.__len__() - 1], ".")
    directorio = "templates/"
    path = directorio + fich[0].lower() + ".html"
    
    return path

def nomPlatilla(fichPy):
    sep = "/"
    if str.find(fichPy,"\\") != -1:
        sep = "\\"
    arr = str.split(fichPy, sep)
    fich = str.split(arr[arr.__len__() - 1], ".")
    
    return fich[0].lower() + ".html"

def tiempo(fecha):
    desde = "Hace "
    temp = datetime.today() - fecha
    if temp.days > 0:
        desde = str(temp.days)
        if temp.days == 1:
            desde = desde + " d&iacute;a"
        else:
            desde = desde + " d&iacute;as"
    elif temp.seconds > 0:
        if round((temp.seconds / 60) / 60) > 1:
            desde = str(round((temp.seconds / 60) / 60))
            if round((temp.seconds / 60) / 60) == 1:
                desde = desde + " hora"
            else:
                desde = desde + " horas"
        elif round(temp.seconds / 60) > 1:
            desde = str(round(temp.seconds / 60))
            if round(temp.seconds / 60) == 1:

                desde = desde + " minuto"
            else:
                desde = desde + " minutos"
        else:
            desde = str(temp.seconds)
            if temp.seconds == 1:
                desde = desde + " segundo"
            else:
                desde = desde + " segundos"
    return desde

def meses():
    meses = []
    for i in range(1,13):
        obj = {}
        mes = i
        if i < 10:
            mes = '0' + str(i)
        obj["id"] = mes
        obj["desc"] = time.strftime("%B", time.strptime("01/" + str(mes) + "/2012", "%d/%m/%Y"))
        meses.append(obj)
    return meses

def anios():
    anios = []
    obj = {}
    obj["id"] = time.strftime("%Y")
    obj["desc"] = time.strftime("%Y")
    anios.append(obj)
    for i in range(1,13):
        obj = {}
        anio = time.strftime("%Y")
        anio = str(int(anio) - i)
        obj["id"] = anio
        obj["desc"] = anio
        anios.append(obj)
    return anios