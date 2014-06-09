import unittest

import mock

from pywall.funnycats.funnycats import FunnyCats
from pywall.funnycats.user import User, get_user_list_score


class TestsUser(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.jenkins = mock.Mock()

	def setUp(self):
		self.funnycats = FunnyCats(self.jenkins, "Score", "funnycats_tests")
		self.funnycats.connect_db()
		self.funnycats.clear_db()

		self.user1 = User()
		self.user1.name = "User1"
		self.user1.score = 3
		self.user1.save()

		self.user2 = User()
		self.user2.name = "User2"
		self.user2.score = 10
		self.user2.save()

		self.user3 = User()
		self.user3.name = "User3"
		self.user3.score = 9
		self.user3.save()


	def tearDown(self):
		self.funnycats.disconnect_db()


	def test_get_user_list_score(self):
		users = get_user_list_score()
		self.assertTrue(3, len(users))
		self.assertEquals(self.user2.name, users[0]["name"])
		self.assertEquals(self.user3.name, users[1]["name"])
		self.assertEquals(self.user1.name, users[2]["name"])