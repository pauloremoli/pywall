__author__ = 'paulo'

from mongoengine import *


class User(Document):
	name = StringField(required=True)
	score = IntField(default=0)

