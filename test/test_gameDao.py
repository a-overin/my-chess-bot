import unittest
from unittest.mock import patch
from src.game.gameDao import GameDao
from src.game.gameSettings import GameStatuses


def mock_create_game():
    return -1


class TestGameDao(unittest.TestCase):

    def setUp(self) -> None:
        self.dao = GameDao()

    def test_get_game_for_room(self):
        game = self.dao.get_game_for_room(-1, GameStatuses.started())
        print(game)
        assert len(game) == 0

    @patch("src.game.gameDao.GameDao.create_game_for_room", side_effect=mock_create_game)
    def test_create_game_for_room(self, create_game):
        print(create_game())


if __name__ == '__main__':
    unittest.main()
