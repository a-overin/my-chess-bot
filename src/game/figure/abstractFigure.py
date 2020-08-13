from abc import ABC, abstractmethod
from ..board.boardCell import Cell


class FigureTypes:

    @classmethod
    def king(cls):
        return 0

    @classmethod
    def queen(cls):
        return 1

    @classmethod
    def rook(cls):
        return 2

    @classmethod
    def bishop(cls):
        return 3

    @classmethod
    def knight(cls):
        return 4

    @classmethod
    def pawn(cls):
        return 5


class AbstractFigure(ABC):

    def __init__(self, position: Cell) -> None:
        self.cell = position

    @abstractmethod
    def can_move(self, new_position: Cell) -> bool:
        # Проверяем может ли фигура пойти на новую позицию
        pass

    @classmethod
    @abstractmethod
    def get_type_id(cls) -> int:
        pass
