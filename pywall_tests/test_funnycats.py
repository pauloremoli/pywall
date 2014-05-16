import unittest

import mock

from pywall.funnycats.funnycats import *


class TestFunnyCats(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.jenkins = mock.Mock()
		cls.jenkins.get_user_list.return_value = [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}]
		cls.jenkins.get_culprits.return_value = [{"fullName": "User1"}, {"fullName": "User2"}]


	def setUp(self):
		self.funnycats = FunnyCats(self.jenkins, "Score", "funnycats_tests")
		self.funnycats.init()
		self.funnycats.clear_db()

		user = User()
		user.name = "User1"
		user.score = 10
		user.save()

	def tearDown(self):
		self.funnycats.clear_db()


	def test_all_users_are_in_db(self):
		self.assertTrue(self.funnycats.init())
		for user in self.jenkins.get_user_list(self.jenkins):
			assert User.objects(name=user["name"]).first is not None


	def test_no_connection(self):
		self.funnycats.connect_db = mock.MagicMock()
		self.funnycats.connect_db.return_value = False

		self.assertFalse(self.funnycats.init())
		self.assertFalse(self.funnycats.is_connected())

		self.assertFalse(self.funnycats.is_connected())


	def test_update_score_build_success(self):
		job = mock.Mock()
		build = mock.Mock()
		build.is_running.return_value = False
		build.get_status.return_value = 'SUCCESS'

		self.jenkins.get_bonus_per_build.return_value = 2

		self.funnycats.is_connected = mock.MagicMock()
		self.funnycats.is_connected.return_value = True

		user1 = User.objects(name="User1").first()
		self.assertEquals(10, user1.score)

		self.assertTrue(self.funnycats.update_score_build(job, build))

		user2 = User.objects(name="User2").first()

		user1.reload()
		user2.reload()
		self.assertEquals(13, user1.score)
		self.assertEquals(3, user2.score)

		self.assertTrue(self.funnycats.update_score_build(job, build))

		user1.reload()
		user2.reload()
		self.assertEquals(16, user1.score)
		self.assertEquals(6, user2.score)

	def test_update_score_build_failure(self):
		job = mock.Mock()
		build = mock.Mock()
		build.is_running.return_value = False
		build.get_status.return_value = 'FAILURE'

		self.jenkins.get_bonus_per_build.return_value = 0
		self.funnycats.is_connected = mock.MagicMock()
		self.funnycats.is_connected.return_value = True

		user1 = User.objects(name="User1").first()
		self.assertEquals(10, user1.score)

		self.assertTrue(self.funnycats.update_score_build(job, build))

		user1.reload()
		self.assertEquals(5, user1.score)

		self.jenkins.get_bonus_per_build.return_value = 6

		self.assertTrue(self.funnycats.update_score_build(job, build))

		user1.reload()
		self.assertEquals(-25, user1.score)

	def test_update_score_build_building(self):
		job = mock.Mock()
		build = mock.Mock()
		build.is_running.return_value = True
		build.get_status.return_value = 'FAILURE'

		self.jenkins.get_bonus_per_build.return_value = 0
		self.funnycats.is_connected = mock.MagicMock()
		self.funnycats.is_connected.return_value = True

		user1 = User.objects(name="User1").first()
		self.assertEquals(10, user1.score)

		self.assertFalse(self.funnycats.update_score_build(job, build))

		user1.reload()
		self.assertEquals(10, user1.score)

		build.is_running.return_value = False
		self.assertTrue(self.funnycats.update_score_build(job, build))

		user1.reload()
		self.assertEquals(5, user1.score)

	def test_update_user_score(self):
		self.jenkins.get_bonus_per_build.return_value = 0

		job_status = {
		'project': "Job1",
		'last_build': 1,
		'status': 'SUCCESS',
		'previousBuildStatus': None
		}

		score_job = ScoreJob()
		score_job.name = "Job1"
		score_job.save()

		build = mock.Mock()
		build.is_running.return_value = False
		build.get_status.return_value = 'FAILURE'

		job = mock.Mock()
		job.get_build.return_value = build
		self.jenkins.get_job.return_value = job

		self.assertTrue(self.funnycats.update_user_score(job_status))

		user1 = User.objects(name="User1").first()
		self.assertEquals(5, user1.score)

		user2 = User.objects(name="User2").first()
		self.assertEquals(-5, user2.score)

		score_job.reload()
		self.assertEquals(1, score_job.last_build_number)


if __name__ == '__main__':
	unittest.main()
