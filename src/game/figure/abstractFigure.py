from abc import ABC, abstractmethod
from ..board.boardCell import Cell


class FigureTypes:

    @classmethod
    def king(cls):
        return 0, 'K'

    @classmethod
    def queen(cls):
        return 1, 'Q'

    @classmethod
    def rook(cls):
        return 2, 'R'

    @classmethod
    def bishop(cls):
        return 3, 'B'

    @classmethod
    def knight(cls):
        return 4, 'N'

    @classmethod
    def pawn(cls):
        return 5, 'P'


class AbstractFigure(ABC):

    def __init__(self, position: Cell) -> None:
        self.cell = position

    @abstractmethod
    def can_move(self, new_position: Cell) -> bool:
        # Проверяем может ли фигура пойти на новую позицию
        pass

    @abstractmethod
    def get_type_id(self) -> tuple:
        pass
