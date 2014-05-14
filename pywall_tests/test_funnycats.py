import unittest

import mock

from pywall.funnycats.funnycats import *


class TestFunnyCats(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.jenkins = mock.Mock()
		cls.jenkins.get_user_list.return_value = [{"name": "User1"}, {"name": "User2"}, {"name": "User3"}]
		cls.funnycats = FunnyCats(cls.jenkins, "Score", "funnycats_tests")


	def test_all_users_are_in_db(self):
		self.assertTrue(self.funnycats.init())
		self.assertEquals(len(self.jenkins.get_user_list(self.jenkins)), len(User.objects()))

	def test_no_connection(self):
		self.funnycats.connect_db = mock.MagicMock()
		self.funnycats.connect_db.return_value = False

		self.assertFalse(self.funnycats.init())


	def test_has_user_with_same_name(self):
		user_list = []
		for user in User.objects():
			self.assertFalse(user_list.__contains__(user.name))
			user_list.append(user.name)

	@classmethod
	def tearDownClass(cls):
		cls.funnycats.disconnect_db()
		cls.funnycats.is_connected()
		cls.funnycats.clear_db()


if __name__ == '__main__':
	unittest.main()
