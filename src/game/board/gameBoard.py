import json
from datetime import datetime as dt
from .imageUtils import Utils
from ..figure.abstractFigure import AbstractFigure


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

    def __init__(self, board_type: int, figure_positions: dict, board_picture: BoardPictureTypeStandard, max_letter='H', max_number=8) -> None:
        self.type = board_type
        self.figure_positions = figure_positions
        self.max_letter = max_letter
        self.max_number = max_number
        self.board_picture = board_picture
        self.figure_path = "/chess_figures/merida/{}.png"

    @classmethod
    def get_json_from_positions(cls, positions: dict) -> str:
        # получаем json из словаря позиций
        return json.dumps(positions)

    @classmethod
    def get_position_from_json(cls, pos: str) -> dict:
        # получаем позиции из json'a
        return json.loads(pos)

    def get_picture(self):
        n = dt.now()
        figure_cache = {}
        i_util = Utils(self.board_picture.cell_size,
                       self.board_picture.lift_size_x,
                       self.board_picture.lift_size_y)
        board = i_util.get_image(self.board_picture.path)
        print("get board" + str(dt.now() - n))
        for k, v in self.figure_positions.items():
            figure = figure_cache.get(self.figure_path.format(v))
            if figure is None:
                figure = i_util.get_image(self.figure_path.format(v), need_resize=True)
                figure_cache[self.figure_path.format(v)] = figure
            print("get {} ".format(v) + str(dt.now() - n))
            i_util.set_position(board, figure, k)
            print("set_position {} ".format(v) + str(dt.now() - n))
        file = i_util.get_file_from_image(board)
        print("file " + str(dt.now() - n))
        return file

    def figure_delete(self, position) -> bool:
        # удаляем фигуру споля
        pass

    def figure_add(self, figure: AbstractFigure) -> bool:
        # ставим фигуру на поле
        pass

