from .abstractGame import AbstractGame
from .board.boardCell import Cell
from .figure.abstractFigure import AbstractFigure


class StandardGame(AbstractGame):
    def check_user_turn(self, user_id: int) -> bool:
        if self.user_turn == user_id:
            return True

    def validate_move(self, fig: AbstractFigure, new_cell: Cell) -> bool:
        figure_new_cell = self.board.get_figure(new_cell)
        if figure_new_cell is not None and figure_new_cell.color == self.user_color:
            return False
        return fig.can_move(new_cell)

