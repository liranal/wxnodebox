#!/usr/bin/python
# -*- coding: iso-8859-1 -*- 


class Event:
	pass

class EventsManager:
	def __init__(self):
		self.events = []

	def add_event(self, event):
		self.events.append( event)

	def create_event(self, subject):
		event = Event()
		#event.name = event_name
		event.subject = subject
		self.events.append( event)        
		return event

