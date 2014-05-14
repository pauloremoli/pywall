__author__ = 'paulo'

from mongoengine import *


class ScoreJob(Document):
	name = StringField(required=True)
	last_build_number = IntField(default=0)
	last_build_status = StringField()


def need_to_add_job(job_name):
	if job_name is None:
		return False

	if ScoreJob.objects(name=job_name).count() == 0:
		return True
	else:
		return False


def get_bonus_per_build(job):
	return len(job.get_downstream_jobs())