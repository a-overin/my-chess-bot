from unittest import TestCase
from user.user_dao import UserDao


class TestUserDao(TestCase):

    def test_get_user(self):
        dao = UserDao()
        assert len(dao.get_user(1)) == 0
