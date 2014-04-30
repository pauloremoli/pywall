__author__ = 'Paulo'

from mongoengine import connect, ConnectionError

from score_job import ScoreJob
from user import User
from service import client


class FunnyCats():
	def __init__(self, jenkins, score_view, dbname):
		self.score_view = score_view
		self.dbname = dbname
		self.is_connected = False
		self.jenkins = jenkins

		try:
			connect(dbname)
			self.is_connected = True
		except ConnectionError:
			print ("Connection error")
			self.is_connected = False

	def is_connected(self):
		return self.is_connected

	def need_to_add_job(self, job_name):
		if job_name is None:
			return False

		if ScoreJob.objects(name=job_name).count() == 0:
			return True
		else:
			return False


	def get_bonus_per_build(self, job):
		bonus_count = 0
		for downstream_job in job.get_downstream_jobs():
			bonus_count += 1
			bonus_count += self.get_bonus_per_build(downstream_job)

		return bonus_count


	def clear_score(self):
		User.objects().update(set__score=0)


	def update_score_build(self, job, build):
		updated = False
		for culprit in build._data["culprits"]:
			username = culprit["fullName"]
			user = User.objects(name=username).first()
			if user is None:
				user = User(name=username)
				user.save()

			user_score = user.score
			bonus = self.get_bonus_per_build(job)

			if not build.is_running():
				if build.get_status() == 'FAILURE':
					user_score += bonus + 1 * -5
				elif build.get_status() == 'SUCCESS':
					user_score += bonus + 1

				user.update(set__score=user_score)
				user.reload()
				print "Score updated", user.to_json()
				updated = True

		return updated


	def update_user_score(self, job_status):
		score_job = ScoreJob.objects(name=job_status["project"]).first()

		score_last_build_number = score_job.last_build_number
		if score_last_build_number == job_status["last_build"]:
			return

		job = self.jenkins.get_job(job_status["project"])
		for build_number in range(score_last_build_number + 1, job_status["last_build"] + 1):

			build = job.get_build(build_number)
			if self.update_score_build(job, build):
				score_job.update(set__last_build_number=build_number)
			else:
				score_job.update(set__last_build_number=build_number)
				print ("Nothing to update score from job %s" % job_status["project"] )


	def update_view_score(self):
		for job_status in client.get_view_status(self.jenkins, self.score_view):
			last_build_number = job_status["last_build"]
			last_build_status = job_status["status"]

			if self.need_to_add_job(job_status["project"]):
				scoreJob = ScoreJob(name=job_status["project"], last_build_number=last_build_number,
				                    last_build_status=last_build_status)
				print "Addded", scoreJob.to_json()
				scoreJob.save()

			if job_status is not None:
				self.update_user_score(job_status)

	def get_user_list_score(self):
		users_score = []
		for user in User.objects().order_by('score'):
			users_score.append({"name": user.name, "score": user.score})
		return users_score

