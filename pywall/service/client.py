# -*- coding: utf-8 -*-
import time
from jenkinsapi.api import Jenkins
from jenkinsapi.job import Job
from jenkinsapi.build import Build
from jenkinsapi.view import View
from jenkinsapi.views import Views
from jenkinsapi.jenkinsbase import JenkinsBase

def get_jenkins():
 	jenkinsurl = "http://192.168.3.99:8080/jenkins"
	return Jenkins( jenkinsurl )

def get_user_list_score():
	jenkins = get_jenkins()
	userList = []
	urlJSON = jenkins.get_data(jenkins.base_server_url() + '/asynchPeople/api/python')
	userListJSON = urlJSON['users']
	for userJSON in userListJSON:
		user = userJSON['user']
		userURL = user['absoluteUrl']
		userInfo = get_user_info_by_url(userURL)
		properties = userInfo['property']
		userName = userInfo['fullName']
		score = None
		avatarURL = None
		for property_item in properties:
			if(property_item.has_key('participatingInGame')):
				if(property_item['participatingInGame'] == False):
					score = None
					break				
			if(property_item.has_key('score')):
				score = property_item['score']
			if(property_item.has_key('avatarUrl')):
				avatarURL = property_item['avatarUrl']
		if(score is None):
			continue
		if(userExists(userList, userName)):
			appendScoreToUser(userList, userName, score)
		else:
			userDict = {'name':userName, 'score':score, 'avatar':avatarURL}
			userList.append(userDict)
	return userList

def appendScoreToUser(userList, userName, score):
	for user in userList:
		if(user['name'] == userName):
			newScore = user['score'] + score
			user.update( {'score': newScore} )

def userExists(userList, userName):
	for user in userList:
		if(userName in user.values()):
			return True
	
	return False

def get_user_info_by_url(url):
	jenkins = get_jenkins()
	urlJSON = jenkins.get_data(url + '/api/python')
	return urlJSON

def get_last_failure():
	jenkins = get_jenkins()
	last_failed_build_date = None
	culprits = []
	broken_jobs = []
	for item in jenkins.get_jobs():
		job = jenkins.get_job( item[0] )

		if(job._data['color'] == "disabled"):
			continue

		last_build = job.get_last_build_or_none()
		build = job.get_last_failed_build()
		if( ( build is not None ) and ( last_build is not None ) and ( last_build.get_number() == build.get_number() ) ):
			broken_jobs.append( job.name )
			for culprit in build.get_culprits():
				culprits.append( culprit['fullName'] )
			continue
		if( build is not None ):
			if( last_failed_build_date is None ):
				last_failed_build_date = build.get_timestamp()
			else:
				if( last_failed_build_date < build.get_timestamp() ):
					last_failed_build_date = build.get_timestamp()

	result = {'culprits':culprits, 'broken_jobs':broken_jobs}
	if( not broken_jobs ):
		result.update( {'last_failed':last_failed_build_date} )
	return result

def get_jobs_status():
	jenkins = get_jenkins()
	jobs = []
	for item in jenkins.get_jobs():
		job = jenkins.get_job( item[0] )
		project = {'project': item[0] }
		build = job.get_last_build_or_none()
		if( build ):
			project.update( {'last_build': build.get_number()} )
			project.update( {'status': build.get_status()} )
			if( build.is_running() ):
				project.update( {'status': 'BUILDING'} )
			# who broke the build
			if( build.get_actions()["causes"][0].has_key( "userId" ) ):
				project.update( {'user': build.get_actions()["causes"][0]["userId"]} )
		else:
			project.update( {'last_build': None} )
		jobs.append( project )

	return jobs

def get_view_status(view_name):
	jenkinsapi = get_jenkins()
	views = Views(jenkinsapi)
	view = views.__getitem__(view_name)
	jobs = []
	for item in view._get_jobs():
		job = jenkinsapi.get_job(item[0])
		project = {'project': item[0] }
		build = job.get_last_build_or_none()
		if( build ):
			project.update( {'last_build': build.get_number()} )
			project.update( {'status': build.get_status()} )

			previousBuild = job.get_build(build.get_number() - 1)
			project.update( {'previousBuildStatus': previousBuild.get_status()} )

			if( build.is_running() ):
				project.update( {'status': 'BUILDING'} )

				estimated = build._data['estimatedDuration']
				completed = (time.time() * 1000) - build._data['timestamp']
				completeRate = (completed * 100) / estimated
				if(completeRate > 99):
					completeRate = 99
				project.update( {'completeRate': completeRate} )

			# who broke the build
			if( build.get_actions()["causes"][0].has_key( "userId" ) ):
				project.update( {'user': build.get_actions()["causes"][0]["userId"]} )
		else:
			project.update( {'last_build': None} )
		jobs.append( project )

	return jobs