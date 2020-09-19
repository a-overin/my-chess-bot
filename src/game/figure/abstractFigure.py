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

    def __init__(self, position: Cell, color: str) -> None:
        self.cell = position
        self.color = color
        self.text = "Color:{color}, Position:{position}, Type:{type}"

    @abstractmethod
    def can_move(self, new_position: Cell) -> bool:
        # Проверяем может ли фигура пойти на новую позицию
        pass

    @abstractmethod
    def get_type_id(self) -> tuple:
        pass

    def __str__(self) -> str:
        return self.text.format(color="white" if self.color == 'w' else "black",
                                position=self.cell,
                                type=self.__class__.__name__)

    def __repr__(self) -> str:
        return self.text.format(color="white" if self.color == 'w' else "black",
                                position=self.cell,
                                type=self.__class__.__name__)


