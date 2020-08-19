from .userDao import UserDao
from .userModel import UserModel
import logging


logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, dao=UserDao) -> None:
        self.dao = dao()

    def check_user(self, telegram_id: int) -> bool:
        try:
            user = self.dao.get_user(telegram_id)
            if user is None:
                self.dao.create_user(telegram_id)
            else:
                return True
            user = self.dao.get_user(telegram_id)
            if user is None:
                return False
            return True
        except Exception as e:
            logger.error("error while check user", e)
            return False

    def get_user(self, telegram_id) -> UserModel:
        user = self.dao.get_user(telegram_id)
        return UserModel(user[0], user[1], user[2])
