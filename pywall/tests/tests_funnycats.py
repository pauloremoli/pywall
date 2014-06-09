import unittest

import mock

from pywall.funnycats.funnycats import *


class TestFunnyCats(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.jenkins = mock.Mock()
		cls.job = mock.Mock()
		cls.build = mock.Mock()


	def setUp(self):
		self.job_status = {
		'project': "Job1",
		'last_build': 2,
		'status': 'SUCCESS',
		'previousBuildStatus': 'SUCCESS'
		}

		job2_status = {
		'project': "Job2",
		'last_build': 5,
		'status': 'FAILURE',
		'previousBuildStatus': 'FAILURE'
		}

		job3_status = {
		'project': "Job3",
		'last_build': 10,
		'status': 'SUCCESS',
		'previousBuildStatus': 'FAILURE'
		}

		self.view_status = [self.job_status, job2_status, job3_status]

		self.jenkins.get_user_list.return_value = [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}]
		self.jenkins.get_culprits.return_value = [{"fullName": "User1"}, {"fullName": "User2"}]
		self.jenkins.get_view_status.return_value = self.view_status
		self.build.get_number_return_value = 1
		self.build.is_running.return_value = False
		self.build.get_status.return_value = 'SUCCESS'
		self.jenkins.get_bonus_per_build.return_value = 0

		self.job.get_build.return_value = self.build
		self.jenkins.get_job.return_value = self.job

		self.funnycats = FunnyCats(self.jenkins, "Score", "funnycats_tests")
		self.funnycats.init()
		self.funnycats.clear_db()

		user = User()
		user.name = "User1"
		user.score = 10
		user.save()

		score_job = ScoreJob()
		score_job.name = "Job1"
		score_job.last_build_number = 1
		score_job.last_build_status = 'SUCCESS'
		score_job.save()


	def tearDown(self):
		self.funnycats.clear_db()


	def test_all_users_are_in_db(self):
		self.funnycats.insert_users_from_server()
		for user in self.jenkins.get_user_list(self.jenkins):
			assert User.objects(name=user["name"]).first is not None


	def test_no_connection(self):
		self.funnycats.connect_db = mock.MagicMock()
		self.funnycats.connect_db.return_value = False

		self.assertFalse(self.funnycats.init())
		self.assertFalse(self.funnycats.is_connected())


	def test_update_score_build_success(self):
		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))
		user1 = User.objects(name="User1").first()
		user2 = User.objects(name="User2").first()

		self.assertEquals(11, user1.score)
		self.assertEquals(1, user2.score)


	def test_consecutive_builds(self):
		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))
		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))
		user1 = User.objects(name="User1").first()
		user2 = User.objects(name="User2").first()
		self.assertEquals(12, user1.score)
		self.assertEquals(2, user2.score)


	def test_update_score_build_failure(self):
		self.build.get_status.return_value = 'FAILURE'

		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))
		user1 = User.objects(name="User1").first()
		user2 = User.objects(name="User2").first()
		self.assertEquals(5, user1.score)
		self.assertEquals(-5, user2.score)


	def test_max_bonus_per_downstream_project(self):
		self.jenkins.get_bonus_per_build.return_value = 10

		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))
		user1 = User.objects(name="User1").first()
		user2 = User.objects(name="User2").first()
		self.assertEquals(16, user1.score)
		self.assertEquals(6, user2.score)


	def test_update_score_build_running(self):
		self.build.is_running.return_value = True
		self.build.get_status.return_value = 'FAILURE'

		self.assertFalse(self.funnycats.update_score_build(self.job, self.build))
		user1 = User.objects(name="User1").first()
		self.assertEquals(10, user1.score)

		self.build.is_running.return_value = False
		self.assertTrue(self.funnycats.update_score_build(self.job, self.build))

		user1.reload()
		self.assertEquals(5, user1.score)


	def test_update_user_score(self):
		self.assertTrue(self.funnycats.update_user_score(self.job_status))

		user1 = User.objects(name="User1").first()
		self.assertEquals(11, user1.score)

		user2 = User.objects(name="User2").first()
		self.assertEquals(1, user2.score)

		score_job = ScoreJob.objects(name="Job1").first()
		self.assertEquals(2, score_job.last_build_number)


	def test_update_user_score_with_two_builds_behind(self):
		self.job_status["last_build"] = 3
		self.assertTrue(self.funnycats.update_user_score(self.job_status))

		user1 = User.objects(name="User1").first()
		self.assertEquals(12, user1.score)

		user2 = User.objects(name="User2").first()
		self.assertEquals(2, user2.score)

		score_job = ScoreJob.objects(name="Job1").first()
		self.assertEquals(3, score_job.last_build_number)

	def test_update_view_score(self):
		self.funnycats.update_view_score()

		job1 = ScoreJob.objects(name='Job1').first()
		self.assertEquals(2, job1.last_build_number)
		job2 = ScoreJob.objects(name='Job2').first()
		self.assertEquals(5, job2.last_build_number)
		job3 = ScoreJob.objects(name='Job3').first()
		self.assertEquals(10, job3.last_build_number)


if __name__ == '__main__':
	unittest.main()
