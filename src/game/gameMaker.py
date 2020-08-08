from .abstractGame import AbstractGame
from .gameDao import GameDao


class GameMaker:

    def __init__(self) -> None:
        self.game_dao = GameDao()

    def get_game_for_chat_room(self, chat_room: int) -> AbstractGame:
        self.game_dao.get_game_for_room(chat_room)
