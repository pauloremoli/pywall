__author__ = 'paulo'

from mongoengine import Document, StringField, IntField


class User(Document):
	name = StringField(required=True, unique=True)
	score = IntField(default=0)


def clear_score():
	User.objects().update(set__score=0)


def get_user_list_score(self):
	users_score = []
	for user in User.objects().order_by('-score'):
		users_score.append({"name": user.name, "score": user.score})
	return users_score
