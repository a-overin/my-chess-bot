from abc import ABC, abstractmethod
from datetime import datetime as dt
import logging
from chess import Piece, UNICODE_PIECE_SYMBOLS
from .gameDao import GameDao
from .board.gameBoard import GameBoard
from .gameSettings import GameStatuses

logger = logging.getLogger(__name__)


class AbstractGame(ABC):

    def __init__(self, game_id: int, game_board: GameBoard, gamers: list, status: int, turn_number: int, user_turn: int, user_color: bool) -> None:
        self.id = game_id
        self.board = game_board
        self.gamers = gamers
        self.status = status
        self.dao = GameDao()
        self.turn_number = turn_number
        self.user_turn = user_turn
        self.user_color = user_color

    def user_in_game(self, user_id: int) -> bool:
        return user_id in self.gamers

    @abstractmethod
    def check_user_turn(self, user_id: int) -> bool:
        # проверяем может ли ходить данный пользователь
        pass

    def make_turn(self, user_id: int, turn: str) -> bool:
        if not self.check_user_turn(user_id):
            return False
        try:
            save_turn = self.board.board.push_san(turn)
        except ValueError as error:
            logger.error(error)
            return False
        self.dao.save_table_positions(self.id,
                                      self.turn_number + 1,
                                      self.user_turn,
                                      save_turn.uci())
        if self.board.board.is_game_over():
            # ``1 - 0``, ``0 - 1`` or ``1 / 2 - 1 / 2``
            result = self.board.board.result()
            if result == "1 - 0":
                logger.info("white win " + str(self.id))
                self.dao.edit_game(self.id, GameStatuses.white_win(), end_time=dt.now())
            elif result == "0 - 1":
                logger.info("black win " + str(self.id))
                self.dao.edit_game(self.id, GameStatuses.black_win(), end_time=dt.now())
            else:
                logger.info("draw " + str(self.id))
                self.dao.edit_game(self.id, GameStatuses.draw(), end_time=dt.now())
        return True

    def get_figures_for_move(self) -> set:
        return self.board.get_figures_move()

    def get_available_for_figure(self, figure: str) -> set:
        piece = Piece.from_symbol([k for k, v in UNICODE_PIECE_SYMBOLS.items() if v == figure][0])
        return self.board.get_move_for_figure(piece)

    def get_results(self) -> tuple:
        if self.board.board.is_game_over():
            # ``1 - 0``, ``0 - 1`` or ``1 / 2 - 1 / 2``
            result = self.board.board.result()
            if result == "1 - 0":
                return True, "White win"
            elif result == "0 - 1":
                return False, "Black win"
            else:
                return None, "Draw"
