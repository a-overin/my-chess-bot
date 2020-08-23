from .abstractGame import AbstractGame
from .standartGame import StandardGame
from .gameSettings import GameStatuses, GameType
from .gameDao import GameDao
from .board.gameBoard import GameBoard
from ..exceptions import GameNotFoundException
from datetime import datetime as dt
import random


class GameMaker:

    def __init__(self, dao=GameDao()) -> None:
        self.game_dao = dao

    def get_game_for_chat_room(self, room_id: int) -> AbstractGame:
        find_game = self.game_dao.get_game_for_room(room_id)
        if len(find_game) == 0:
            raise GameNotFoundException()
        positions = self.game_dao. get_table_positions(find_game.get("id"))
        positions = positions.get("table_position") or positions.get("table_start_position")
        board = GameBoard(find_game.get("game_type"),
                          GameBoard.get_position_from_json(positions))
        player_list = self.game_dao.get_game_users(find_game.get("id"))
        game = StandardGame(find_game.get("id"),
                            board,
                            player_list,
                            find_game.get("game_status"))
        return game

    def accept_game(self, room_id: int, user_id: int) -> AbstractGame:
        game = self.get_game_for_chat_room(room_id)
        # принимаем игру
        if game.status != GameStatuses.created():
            raise Exception("Game already start")
        users = self.game_dao.get_game_users(game.id)
        if user_id in [user.get("user_id") for user in users]:
            raise Exception("You are already in game")
        color = self.get_user_color(users)
        self.game_dao.add_user_for_game(game.id, user_id, color)
        self.game_dao.edit_game(game.id, GameStatuses.started(), dt.now())
        return game

    def create_game(self, room_id: int, user_id: int) -> AbstractGame:
        try:
            self.get_game_for_chat_room(room_id)
            raise Exception("Game already created")
        except GameNotFoundException:
            pass
        game_id = self.game_dao.create_game_for_room(room_id, GameType.standard())
        if game_id is not None:
            color = self.get_user_color([])
            self.game_dao.add_user_for_game(game_id, user_id, color)
        else:
            raise Exception("Cannot create game")
        game = self.get_game_for_chat_room(room_id)
        return game

    @staticmethod
    def get_user_color(users: list) -> bool:
        if len(users) == 1:
            return True if users[0].get("user_color") == 0 else False
        return random.randrange(2)
