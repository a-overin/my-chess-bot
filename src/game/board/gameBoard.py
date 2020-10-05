from datetime import datetime as dt
from typing import List, Set
from chess import Board, Piece, STARTING_FEN, square_name

from .imageUtils import Utils


class BoardPictureTypeStandard:

    def __init__(self) -> None:
        self.path = "/boards/standard.png"
        self.cell_size = 81
        self.lift_size_x = 53
        self.lift_size_y = 55


class BoardPictureTypeBlackWhite(BoardPictureTypeStandard):

    def __init__(self) -> None:
        super().__init__()
        self.path = "/boards/board_bw.png"
        self.cell_size = 59
        self.lift_size_x = 23
        self.lift_size_y = 25


class GameBoard:

    def __init__(self, board_type: int,
                 board: Board,
                 board_picture: BoardPictureTypeStandard, ) -> None:
        self.type = board_type
        self.board = board
        self.board_picture = board_picture
        self.figure_path = "/chess_figures/merida/{}.png"

    @classmethod
    def get_game_from_moves(cls, moves: List[str], start_position: str = STARTING_FEN) -> Board:
        board = Board(fen=start_position)
        if moves[-1][1] is not None:
            [board.push_uci(move[1]) for move in moves]
        return board

    def get_picture(self):
        n = dt.now()
        figure_cache = {}
        i_util = Utils(self.board_picture.cell_size,
                       self.board_picture.lift_size_x,
                       self.board_picture.lift_size_y)
        board = i_util.get_image(self.board_picture.path)
        print("get board" + str(dt.now() - n))
        for k, v in self.board.piece_map().items():
            fig = 'w' if v.color else 'b'
            fig += str(v).upper()
            figure = figure_cache.get(self.figure_path.format(fig))
            if figure is None:
                figure = i_util.get_image(self.figure_path.format(fig), need_resize=True)
                figure_cache[self.figure_path.format(fig)] = figure
            print("get {} ".format(fig) + str(dt.now() - n))
            i_util.set_position(board, figure, square_name(k))
            print("set_position {} ".format(fig) + str(dt.now() - n))
        file = i_util.get_file_from_image(board)
        print("file " + str(dt.now() - n))
        return file

    def get_figures_move(self) -> Set[str]:
        all_moves = self.board.legal_moves
        avail_fig = set([self.board.piece_at(move.from_square).unicode_symbol() for move in all_moves])
        return avail_fig

    def get_move_for_figure(self, figure: Piece) -> Set[str]:
        all_moves = self.board.legal_moves
        avail_moves = set([self.board.san(move) for move in all_moves
                           if self.board.piece_at(move.from_square) == figure])
        return avail_moves

    def get_last_move(self) -> str:
        if len(self.board.move_stack) > 1:
            return str(self.board.peek())
        else:
            return ""
