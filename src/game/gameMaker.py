from .abstractGame import AbstractGame
from .gameSettings import GameStatuses, GameType
from .gameDao import GameDao
from datetime import datetime as dt
import random


class GameMaker:

    def __init__(self, dao=GameDao()) -> None:
        self.game_dao = dao

    def get_game_for_chat_room(self, room_id: int) -> AbstractGame:
        started_game = self.game_dao.get_game_for_room(room_id)
        if len(started_game) == 0:
            raise Exception("Game not started")

    def accept_game(self, room_id: int, user_id: int) -> AbstractGame:
        game = self.game_dao.get_game_for_room(room_id)
        # принимаем игру
        if len(game) != 0:
            if game.get("game_status") != GameStatuses.created():
                raise Exception("Game already start")
            users = self.game_dao.get_game_users(game.get("id"))
            if user_id in [user.get("user_id") for user in users]:
                raise Exception("You are already in game")
            color = self.get_user_color(users)
            self.game_dao.add_user_for_game(game.get("id"), user_id, color)
            self.game_dao.edit_game(game.get("id"), GameStatuses.started(), dt.now())
        else:
            raise Exception("Game not found")
        #     возвращаем игру
        return game

    def create_game(self, room_id: int, user_id: int) -> AbstractGame:
        game = self.game_dao.get_game_for_room(room_id)
        if len(game) != 0:
            raise Exception("Game already created")
        game_id = self.game_dao.create_game_for_room(room_id, GameType.standard())
        if game_id is not None:
            color = self.get_user_color([])
            self.game_dao.add_user_for_game(game_id, user_id, color)
        else:
            raise Exception("Cannot create game")
        game = self.game_dao.get_game_for_room(room_id)
        return game

    def get_user_color(self, users: list) -> bool:
        if len(users) == 1:
            return True if users[0].get("user_color") == 0 else False
        return random.randrange(2)
