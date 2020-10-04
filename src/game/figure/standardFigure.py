from .abstractFigure import AbstractFigure, FigureTypes
from ..board.boardCell import Cell


class Bishop(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.bishop()


class King(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        numb = abs(self.cell.number - new_position.number)
        let = abs(ord(self.cell.letter) - ord(new_position.letter))
        if (numb == let == 1) or (numb + let == 1):
            return True

    def get_type_id(self) -> tuple:
        return FigureTypes.king()


class Knight(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        numb = abs(self.cell.number - new_position.number)
        let = abs(ord(self.cell.letter) - ord(new_position.letter))
        if (numb == 2 and let == 1) or (numb == 1 and let == 2):
            return True
        return False

    def get_type_id(self) -> tuple:
        return FigureTypes.knight()


class Pawn(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        if abs(ord(self.cell.letter) - ord(new_position.letter)) not in (0, 1):
            return False
        if self.color == 'w':
            if self.cell.number == 2 and self.cell.letter == new_position.letter:
                return new_position.number - self.cell.number in (1, 2)
            else:
                return new_position.number - self.cell.number == 1
        else:
            if self.cell.number == 7 and self.cell.letter == new_position.letter:
                return new_position.number - self.cell.number in (-1, -2)
            else:
                return new_position.number - self.cell.number == -1

    def get_type_id(self) -> tuple:
        return FigureTypes.pawn()


class Queen(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.queen()


class Rook(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        if self.cell.number == new_position.number:
            return not (self.cell.letter == new_position.letter)
        if self.cell.letter == new_position.letter:
            return not (self.cell.number == new_position.number)

    def get_type_id(self) -> tuple:
        return FigureTypes.rook()


standard_figures: {str: AbstractFigure} = {
    FigureTypes.queen()[1]: Queen,
    FigureTypes.knight()[1]: Knight,
    FigureTypes.rook()[1]: Rook,
    FigureTypes.pawn()[1]: Pawn,
    FigureTypes.bishop()[1]: Bishop,
    FigureTypes.king()[1]: King
}
