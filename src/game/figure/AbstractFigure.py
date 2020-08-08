from abc import ABC, abstractmethod


class FigureTypes:
    pass


class AbstractFigure(ABC):

    def __init__(self, letter: str, number: int) -> None:
        # буква, где находится фигруа
        self.letter = letter
        # цифра, где находится фигура
        self.number = number

    @abstractmethod
    def can_move(self, letter: str, numb: int) -> bool:
        # Проверяем может ли фигура пойти на новую позицию
        pass

    @classmethod
    @abstractmethod
    def get_type_id(cls) -> int:
        pass
