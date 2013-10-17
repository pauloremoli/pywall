# -*- coding: utf-8 -*-
from datetime import datetime
from jenkinsapi.api import Jenkins
from jenkinsapi.job import Job
from jenkinsapi.build import Build
from jenkinsapi.view import View
from jenkinsapi.views import Views


def get_jenkins():
#	jenkinsurl = "http://localhost:8080"
 	jenkinsurl = "http://192.168.4.38:8080/jenkins"
	return Jenkins( jenkinsurl )

def get_last_failure():
	jenkins = get_jenkins()
	last_failed_build_date = None
	culprits = []
	broken_jobs = []
	for item in jenkins.get_jobs():
		job = jenkins.get_job( item[0] )
		last_build = job.get_last_build_or_none()
		build = job.get_last_failed_build()
		if( ( build is not None ) and ( last_build is not None ) and ( last_build.get_number() == build.get_number() ) ):
			broken_jobs.append( job )
			if( build.get_culprits() ):
				culprits.append( build._data['culprits'] )
			continue
		if( build is not None ):
			if( last_failed_build_date is None ):
				last_failed_build_date = build.get_timestamp()
			else:
				if( last_failed_build_date < build.get_timestamp() ):
					last_failed_build_date = build.get_timestamp()

			if( build.get_culprits() ):
				culprits = build.get_culprits()

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
			if( build.is_running() ):
				project.update( {'status': 'BUILDING'} )
			# who broke the build
			if( build.get_actions()["causes"][0].has_key( "userId" ) ):
				project.update( {'user': build.get_actions()["causes"][0]["userId"]} )
		else:
			project.update( {'last_build': None} )
		jobs.append( project )

	return jobs

get_view_status("Build")