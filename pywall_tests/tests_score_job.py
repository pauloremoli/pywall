import unittest

import mock

from pywall.funnycats.funnycats import FunnyCats
from pywall.funnycats.score_job import ScoreJob, need_to_add_job


class TestScoreJob(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.jenkins = mock.Mock()

	def setUp(self):
		self.funnycats = FunnyCats(self.jenkins, "Score", "funnycats_tests")
		self.funnycats.connect_db()
		self.funnycats.clear_db()


	def tearDown(self):
		self.funnycats.disconnect_db()

	def test_need_to_add_job(self):
		job = ScoreJob()
		job.name = "Job1"
		job.save()

		self.assertFalse(need_to_add_job("Job1"))
		self.assertTrue(need_to_add_job("Job2"))