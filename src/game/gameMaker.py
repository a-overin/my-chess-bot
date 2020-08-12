from .abstractGame import AbstractGame
from .gameSettings import GameStatuses, GameType
from .gameDao import GameDao
from datetime import datetime as dt


class GameMaker:

    def __init__(self, dao=GameDao()) -> None:
        self.game_dao = dao

    def get_game_for_chat_room(self, room_id: int) -> AbstractGame:
        started_game = self.game_dao.get_game_for_room(room_id, GameStatuses.started())
        if len(started_game) == 0:
            return None

    def accept_game(self, room_id: int, user_id: int) -> AbstractGame:
        game = self.game_dao.get_game_for_room(room_id, GameStatuses.created())
        # создаем игру
        if len(game) == 1:
            self.game_dao.edit_game(game.get("game_id"), GameStatuses.started(), dt.now())
            self.game_dao.add_user_for_game(game.get("game_id"), user_id)
        #     возвращаем игру
        return None

    def create_game(self, room_id: int, user_id: int) -> AbstractGame:
        game_id = self.game_dao.create_game_for_room(room_id, GameType.standard())
        if game_id is not None:
            self.game_dao.add_user_for_game(game_id, user_id)
        game = self.game_dao.get_game_for_room(room_id)
        return game
