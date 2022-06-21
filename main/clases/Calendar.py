#!/usr/bin/python
from google.appengine.ext import db

class Event(db.Model):
    title = db.StringProperty(required=True)
    description = db.TextProperty()
    time = db.DateTimeProperty()
    location = db.TextProperty()
    creator = db.UserProperty()
    edit_link = db.TextProperty()
    gcal_event_link = db.TextProperty()
    gcal_event_xml = db.TextProperty()

class Attendee(db.Model):
    email = db.StringProperty()
    event = db.ReferenceProperty(Event)