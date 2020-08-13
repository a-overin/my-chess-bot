from .abstractFigure import AbstractFigure, FigureTypes
from ..board.boardCell import Cell


class Pawn(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    @classmethod
    def get_type_id(cls) -> int:
        FigureTypes.pawn()
