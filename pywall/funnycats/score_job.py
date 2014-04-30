__author__ = 'paulo'

from mongoengine import *


class ScoreJob(Document):
	name = StringField(required=True)
	last_build_number = IntField(default=0)
	last_build_status = StringField()
