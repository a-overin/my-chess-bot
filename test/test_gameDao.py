import unittest
from unittest.mock import patch
from src.game.gameDao import GameDao


def mock_create_game():
    return -1


class TestGameDao(unittest.TestCase):

    def setUp(self) -> None:
        self.dao = GameDao()

    def test_get_game_for_room(self):
        game = self.dao.get_game_for_room(-1)
        assert len(game) == 0

    @patch("src.game.gameDao.GameDao.create_game_for_room", side_effect=mock_create_game)
    def test_create_game_for_room(self, create_game):
        assert create_game() == -1


if __name__ == '__main__':
    unittest.main()
