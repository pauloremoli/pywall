import logging

from mongoengine import connect, ConnectionError
from mongoengine.connection import disconnect

from pywall.funnycats.config import Config
from pywall.funnycats.score_job import ScoreJob, need_to_add_job
from pywall.funnycats.user import User


class FunnyCats():
	def __init__(self, jenkins, score_view, db_name):
		self.score_view = score_view
		self.db_name = db_name
		self.connected = False
		self.jenkins = jenkins


	def insert_users_from_server(self):
		for user in self.jenkins.get_user_list():
			users = User.objects(name=user["name"])
			if users.count() == 0:
				new_user = User(name=user["name"])
				new_user.save()

	def init(self):

		if self.connect_db():
			self.connected = True
		else:
			self.connected = False
			return False

		return True

	def is_connected(self):
		return self.connected

	def update_score_job(self, job_status):

		if self.connected is False:
			return False

		score_job = ScoreJob.objects(name=job_status["project"]).first()

		score_last_build_number = score_job.last_build_number
		if score_last_build_number == job_status["last_build"]:
			return True

		job = self.jenkins.get_job(job_status["project"])
		for build_number in range(score_last_build_number + 1, job_status["last_build"] + 1):
			build = self.jenkins.get_build(build_number, job)
			if build is None:
				continue

			if self.update_score_build(job, build):
				score_job.update(set__last_build_number=build_number)

		return True


	def update_score_view(self):
		if self.connected is False:
			return False

		if self.jenkins is None:
			return False

		for job_status in self.jenkins.get_view_status(self.score_view):


			last_build_number = job_status["last_build"]
			last_build_status = job_status["status"]
			job_name = job_status["project"]
			logging.debug("Update view score for job: " + job_name)

			if need_to_add_job(job_name):
				scoreJob = ScoreJob(name=job_name, last_build_number=last_build_number,
				                    last_build_status=last_build_status)
				scoreJob.save()
				logging.log(logging.DEBUG, "Inserted job: " + job_name)

			if job_status is not None:
				self.update_score_job(job_status)

		return True


	def update_score_build(self, job, build):

		if self.is_connected() is False:
			return False

		for culprit in self.jenkins.get_culprits(build):
			username = culprit["fullName"]
			user = User.objects(name=username).first()
			if user is None:
				user = User(name=username)
				user.save()
			user_score = user.score
			total_bonus = self.jenkins.get_bonus_per_build(job)
			if total_bonus > 5:
				total_bonus = 5
			points = total_bonus + 1

			if build.is_running():
				return False
			else:
				if build.get_status() == 'FAILURE':
					user_score += points * -5
				elif build.get_status() == 'SUCCESS':
					user_score += points

				logging.log(logging.DEBUG, user.name + " " + str(user.score) + " " + str(user_score))
				user.update(set__score=user_score)
				user.reload()

		return True


	def connect_db(self):
		try:
			connect(self.db_name)
			self.connected = True
			return True
		except ConnectionError:
			print("Connection error")
			self.connected = False
			return False

	def disconnect_db(self):
		if disconnect(self.db_name):
			self.connected = False

	def clear_db(self):
		if self.is_connected():
			User.drop_collection()
			ScoreJob.drop_collection()
			Config.drop_collection()