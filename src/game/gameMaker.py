import logging

from ..user.user_service import UserService
from .abstractGame import AbstractGame
from .standartGame import StandardGame
from .gameSettings import GameStatuses, GameType
from .gameDao import GameDao
from .board.gameBoard import GameBoard, BoardPictureTypeStandard, BoardPictureTypeBlackWhite
from ..exceptions import GameNotFoundException, ChessException
from datetime import datetime as dt
import random

logger = logging.getLogger(__name__)


class GameMaker:

    def __init__(self, dao=GameDao(), user_service=UserService()) -> None:
        self.game_dao = dao
        self.user_service = user_service

    def get_game_for_chat_room(self, room_id: int) -> AbstractGame:
        find_game = self.game_dao.get_game_for_room(room_id)
        print(find_game)
        if len(find_game) == 0 or find_game.get("game_status") not in (GameStatuses.created(), GameStatuses.started()):
            raise GameNotFoundException()
        table_moves_history = self.game_dao.get_table_positions(find_game.get("id"))
        board = GameBoard(find_game.get("game_type"),
                          GameBoard.get_game_from_moves(table_moves_history),
                          BoardPictureTypeBlackWhite())
        player_list = self.game_dao.get_game_users(find_game.get("id"))
        game = StandardGame(find_game.get("id"),
                            board,
                            player_list,
                            find_game.get("game_status"),
                            table_moves_history[-1][4],
                            table_moves_history[-1][2],
                            table_moves_history[-1][3])
        return game

    def accept_game(self, room_id: int, user_id: int) -> AbstractGame:
        game = self.get_game_for_chat_room(room_id)
        # принимаем игру
        if game.status != GameStatuses.created():
            raise ChessException("Game already start")
        users = self.game_dao.get_game_users(game.id)
        if user_id in [user.get("user_id") for user in users]:
            raise ChessException("You are already in game")
        color = self.get_user_color(users)
        self.game_dao.add_user_for_game(game.id, user_id, color)
        self.game_dao.edit_game(game.id, GameStatuses.started(), dt.now())
        return game

    def create_game(self, room_id: int, user_id: int) -> AbstractGame:
        try:
            self.get_game_for_chat_room(room_id)
            raise ChessException("Game already created")
        except GameNotFoundException:
            pass
        game_id = self.game_dao.create_game_for_room(room_id, GameType.standard())
        if game_id is not None:
            color = self.get_user_color([])
            self.game_dao.add_user_for_game(game_id, user_id, color)
        else:
            raise ChessException("Cannot create game")
        game = self.get_game_for_chat_room(room_id)
        return game

    def update_rating(self, chat_id: int, winner_color: bool):
        users = self.game_dao.get_game_users(chat_id)
        for user in users:
            if winner_color is None:
                self.user_service.change_rating(user.get("user_id"), 1)
            elif user.get("user_color") == winner_color:
                self.user_service.change_rating(user.get("user_id"), 10)
            else:
                self.user_service.change_rating(user.get("user_id"), -10)

    @staticmethod
    def get_user_color(users: list) -> bool:
        if len(users) == 1:
            return True if users[0].get("user_color") == 0 else False
        return random.randrange(2)
