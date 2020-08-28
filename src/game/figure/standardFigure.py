from .abstractFigure import AbstractFigure, FigureTypes
from ..board.boardCell import Cell


class Bishop(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.bishop()


class King(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.king()


class Knight(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.knight()


class Pawn(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return  FigureTypes.pawn()


class Queen(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return FigureTypes.queen()


class Rook(AbstractFigure):
    def can_move(self, new_position: Cell) -> bool:
        return True

    def get_type_id(self) -> tuple:
        return  FigureTypes.rook()


standard_figures = {
    FigureTypes.queen()[1]: Queen,
    FigureTypes.knight()[1]: Knight,
    FigureTypes.rook()[1]: Rook,
    FigureTypes.pawn()[1]: Pawn,
    FigureTypes.bishop()[1]: Bishop,
    FigureTypes.king()[1]: King
}
