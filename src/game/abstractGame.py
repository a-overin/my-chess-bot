from abc import ABC, abstractmethod
import logging
from .gameDao import GameDao
from .figure.abstractFigure import Cell
from .figure.standardFigure import standard_figures, AbstractFigure
from .board.gameBoard import GameBoard

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

    def make_turn(self, user_id: int, old_position: Cell, new_position: Cell) -> bool:
        if not self.check_user_turn(user_id):
            return False
        if self.board.figure_positions.get(old_position.get_position()) is None:
            return False
        logger.debug(self.board.figure_positions)
        fig = self.board.figure_positions.get(old_position.get_position())
        logger.debug(old_position.get_position())
        logger.debug(fig)
        fig = standard_figures.get(fig[1])(old_position, 'w' if self.user_color else 'b')
        if fig.can_move(new_position):
            self.board.figure_delete(old_position)
            self.board.figure_add(fig, new_position)
        else:
            return False
        self.dao.save_table_positions(self.id,
                                      self.turn_number + 1,
                                      self.user_turn,
                                      GameBoard.get_json_from_positions(self.board.figure_positions))
        return True

    def get_figures_position_for_color(self, color: bool) -> list:
        pos = self.board.get_figures_for_color('w' if color else 'b')
        return pos

    def get_available_for_position(self, position: Cell) -> list:
        fig = self.board.get_figure(position)
        all_cells = self.board.get_all_cells()
        result = []
        for cell in all_cells:
            if self.validate_move(fig, cell):
                result.append(cell.get_position())
        return result

    @staticmethod
    def validate_move(fig: AbstractFigure, cell: Cell) -> bool:
        return fig.can_move(cell)


