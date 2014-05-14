# -*- coding: utf-8 -*-
import time

from jenkinsapi.api import Jenkins
from jenkinsapi.views import Views


class JenkinsClient():
	def __init__(self, jenkinsurl):
		self.jenkinsurl = jenkinsurl
		self.jenkins = Jenkins(self.jenkinsurl)


	def get_user_list(self):
		userList = []
		urlJSON = self.jenkins.get_data(self.jenkins.base_server_url() + '/asynchPeople/api/python')
		userListJSON = urlJSON['users']
		for userJSON in userListJSON:
			user = userJSON['user']
			userName = user['fullName']
			userDict = {'name': userName}
			userList.append(userDict)
		return userList


	def get_last_failure(self):
		last_failed_build_date = None
		culprits = []
		broken_jobs = []
		for item in self.jenkins.get_jobs():
			job = self.jenkins.get_job(item[0])

			if (job._data['color'] == "disabled"):
				continue

			last_build = job.get_last_build_or_none()
			build = job.get_last_failed_build()
			if (( build is not None ) and ( last_build is not None ) and (
				last_build.get_number() == build.get_number() ) ):
				broken_jobs.append(job.name)
				for culprit in build.get_culprits():
					culprits.append(culprit['fullName'])
				continue
			if ( build is not None ):
				if ( last_failed_build_date is None ):
					last_failed_build_date = build.get_timestamp()
				else:
					if ( last_failed_build_date < build.get_timestamp() ):
						last_failed_build_date = build.get_timestamp()

		result = {'culprits': culprits, 'broken_jobs': broken_jobs}
		if ( not broken_jobs ):
			result.update({'last_failed': last_failed_build_date})
		return result


	def get_jobs_status(self):
		jobs = []
		for item in self.jenkins.get_jobs():
			job = self.jenkins.get_job(item[0])
			project = {'project': item[0]}
			build = job.get_last_build_or_none()
			if ( build ):
				project.update({'last_build': build.get_number()})
				project.update({'status': build.get_status()})
				if ( build.is_running() ):
					project.update({'status': 'BUILDING'})
				# who broke the build
				if ( build.get_actions()["causes"][0].has_key("userId") ):
					project.update({'user': build.get_actions()["causes"][0]["userId"]})
			else:
				project.update({'last_build': None})
			jobs.append(project)

		return jobs


	def get_view_status(self, view_name):
		views = Views(self.jenkins)
		view = views.__getitem__(view_name)
		jobs = []
		for item in view._get_jobs():
			job = self.jenkins.get_job(item[0])
			project = {'project': item[0]}
			build = job.get_last_build_or_none()
			if ( build ):
				project.update({'last_build': build.get_number()})
				project.update({'status': build.get_status()})

				previousBuild = job.get_build(build.get_number() - 1)
				project.update({'previousBuildStatus': previousBuild.get_status()})

				if ( build.is_running() ):
					project.update({'status': 'BUILDING'})

					estimated = build._data['estimatedDuration']
					completed = (time.time() * 1000) - build._data['timestamp']
					completeRate = (completed * 100) / estimated
					if (completeRate > 99):
						completeRate = 99
					project.update({'completeRate': completeRate})

				# who broke the build
				if ( build.get_actions()["causes"][0].has_key("userId") ):
					project.update({'user': build.get_actions()["causes"][0]["userId"]})
			else:
				project.update({'last_build': None})
			jobs.append(project)

		return jobs