from unittest import TestCase
from user.userDao import UserDao


class TestUserDao(TestCase):

    def test_get_user(self):
        dao = UserDao()
        print(dao.get_user(1))
