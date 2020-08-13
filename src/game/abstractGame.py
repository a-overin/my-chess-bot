from abc import ABC, abstractmethod
from .gameDao import GameDao
from .figure import abstractFigure
from game.board.gameBoard import GameBoard


class AbstractGame(ABC):

    def __init__(self, game_id: int, game_board: GameBoard, gamers: list, status: int) -> None:
        self.id = game_id
        self.board = game_board
        self.gamers = gamers
        self.status = status
        self.dao = GameDao()

    def user_in_game(self, user_id: int) -> bool:
        return user_id in self.gamers

    @abstractmethod
    def user_turn(self, user_id: int) -> bool:
        # проверяем может ли ходить данный пользователь
        pass

    def make_turn(self, user_id: int, figure: abstractFigure, new_position: str) -> bool:
        if not self.user_turn(user_id):
            return False
        return True
