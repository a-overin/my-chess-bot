import json
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

    def __init__(self, position: Cell, color: str, is_moved: bool = True) -> None:
        self.cell = position
        self.color = color
        self.is_moved = is_moved

    @abstractmethod
    def can_move(self, new_position: Cell) -> bool:
        # Проверяем может ли фигура пойти на новую позицию
        pass

    @abstractmethod
    def get_type_id(self) -> tuple:
        pass

    def get_str_for_file(self) -> str:
        return self.color + self.get_type_id()[1]

    def __str__(self) -> str:
        text = "Color:{color}, Position:{position}, Type:{type}, Moved:{is_moved}"
        return text.format(color="white" if self.color == 'w' else "black",
                           position=str(self.cell),
                           type=self.__class__.__name__,
                           is_moved=self.is_moved)

    def __repr__(self) -> str:
        result = {k: repr(v) for k, v in self.__dict__.items()}
        result["type"] = self.get_type_id()[1]
        return json.dumps(result)
