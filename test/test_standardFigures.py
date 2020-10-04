from unittest import TestCase

from game.board.gameBoard import GameBoard
from src.game.figure.standardFigure import Pawn, Knight, King, Rook
from src.game.board.boardCell import Cell


class TestFigures(TestCase):

    def setUp(self) -> None:
        self.figure = {}
        self.set_pawns()
        self.set_knight()
        self.set_king()
        self.set_rook()

    def set_pawns(self):
        self.figure[Pawn(Cell('e', 2), 'w')] = (Cell('d', 3), Cell('e', 3), Cell('f', 3), Cell('e', 4))
        self.figure[Pawn(Cell('e', 7), 'b')] = (Cell('d', 6), Cell('f', 6), Cell('e', 6), Cell('e', 5))

    def set_knight(self):
        self.figure[Knight(Cell('d', 4), 'w')] = (Cell('c', 2), Cell('c', 6), Cell('e', 2),
                                                  Cell('e', 6), Cell('b', 3), Cell('b', 5),
                                                  Cell('f', 3), Cell('f', 5))
        self.figure[Knight(Cell('d', 4), 'b')] = (Cell('c', 2), Cell('c', 6), Cell('e', 2),
                                                  Cell('e', 6), Cell('b', 3), Cell('b', 5),
                                                  Cell('f', 3), Cell('f', 5))

    def set_king(self):
        self.figure[King(Cell('d', 4), 'w')] = (Cell('c', 5), Cell('d', 5), Cell('e', 5),
                                                Cell('c', 4), Cell('e', 4),
                                                Cell('c', 3), Cell('d', 3), Cell('e', 3))
        self.figure[King(Cell('d', 4), 'b')] = (Cell('c', 5), Cell('d', 5), Cell('e', 5),
                                                Cell('c', 4), Cell('e', 4),
                                                Cell('c', 3), Cell('d', 3), Cell('e', 3))

    def set_rook(self):
        self.figure[Rook(Cell('d', 4), 'w')] = (Cell('d', 1), Cell('d', 2), Cell('d', 3), Cell('d', 5), Cell('d', 6),
                                                Cell('d', 7), Cell('d', 8),
                                                Cell('a', 4), Cell('b', 4), Cell('c', 4), Cell('e', 4), Cell('f', 4),
                                                Cell('g', 4), Cell('h', 4))
        self.figure[Rook(Cell('d', 4), 'b')] = (Cell('d', 1), Cell('d', 2), Cell('d', 3), Cell('d', 5), Cell('d', 6),
                                                Cell('d', 7), Cell('d', 8),
                                                Cell('a', 4), Cell('b', 4), Cell('c', 4), Cell('e', 4), Cell('f', 4),
                                                Cell('g', 4), Cell('h', 4))

    def test_figures(self):
        message_good = "Figure {} must be able to move {}"
        message_bad = "Figure {} should not be able to move {}"
        board = GameBoard(None, None, None)
        for fig, good_cells in self.figure.items():
            all_cells = board.get_all_cells().copy()
            bad_cells = [cell for cell in all_cells if cell not in good_cells]
            for cell in good_cells:
                self.assertTrue(fig.can_move(cell),
                                message_good.format(fig.__class__.__name__, cell))
            for cell in bad_cells:
                self.assertFalse(fig.can_move(cell),
                                 message_bad.format(fig.__class__.__name__, cell))


