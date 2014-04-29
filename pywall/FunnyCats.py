__author__ = 'Paulo'

from service.client import *
from pymongo import MongoClient

from mongoengine import *



class User(Document):
	name = StringField(required=True)
	score = IntField(default=0)


class ScoreJob(Document):
	name = StringField(required=True)
	lastBuild = IntField(default=0)
	lastBuildStatus = StringField()


class Configuration(Document):
	ignoredJobs = ListField(StringField())
	viewName = StringField()


def needToAddJob(job):
	if job is None:
		return False

	if ScoreJob.objects(name=job).count() == 0:
		return True
	else:
		return False


def getScorePerBuild(job):
	bonusCount = 1
	for downstreamjob in job.get_downstream_jobs():
		bonusCount += 1
		bonusCount += getScorePerBuild(downstreamjob)

	return bonusCount


def clearScore():
	User.objects().update(set__score=0)


def updateScorePerBuild(job, build):
	updated = False
	for culprit in build.get_culprits():
		username = culprit["fullName"]
		user = User.objects(name=username).first()
		if user is None:
			user = User(name=username)
			user.save()

		userScore = user.score
		score = getScorePerBuild(job)

		if not build.is_running():
			if build.get_status() == 'FAILURE':
				userScore += score * -5
			elif build.get_status() == 'SUCCESS':
				userScore += score

			user.update(set__score=userScore)
			user.reload()
			print "Score updated", user.to_json()
			updated = True

	return updated


def updateUserScore(job, lastBuild):
	scorejob = ScoreJob.objects(name=job.name).first()

	lastBuildNumber = scorejob.lastBuild
	if lastBuildNumber == lastBuild.get_number():
		return

	if (lastBuildNumber == 0):
		lastBuildNumber = job.get_first_build().get_number()
	else:
		lastBuildNumber += 1

	for lastBuildNumber in range(lastBuildNumber, lastBuild.get_number()):
		build = job.get_build(scorejob)
		if updateScorePerBuild(job, build):
			scorejob.update(set__lastBuild=lastBuildNumber)
			scorejob.reload()


def updateViewScore(viewName):
	view = jenkins.get_view_by_url(viewName)
	for jobname in view._get_jobs():
		job = jenkins.get_job(jobname[0])
		build = job.get_last_build_or_none()
		lastBuildNumber = 0
		lastBuildStatus = "None"


		if build is not None:
			lastBuildStatus = build.get_status()
			lastBuildNumber = build.get_number()

		if needToAddJob(job.name):
			scoreJob = ScoreJob(name=job.name, lastBuild=lastBuildNumber, lastBuildStatus=lastBuildStatus)
			print "Addded", scoreJob.to_json()
			scoreJob.save()

		if build is not None:
			updateUserScore(job, build)



connect('jenkinci')
#clearScore()

jenkins = get_jenkins("http://192.168.3.99:8080/jenkins")
updateViewScore("http://192.168.3.99:8080/jenkins/view/Wall/")

for user in User.objects():
	print user.name, user.score