__author__ = 'paulo'

from mongoengine import *


class Config(Document):
	ignoredJobs = ListField(StringField())
	viewName = StringField()