import json
from datetime import datetime as dt
from typing import List
from itertools import product

from .imageUtils import Utils
from ..figure.standardFigure import standard_figures, AbstractFigure, Cell


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
                 figure_positions: dict,
                 board_picture: BoardPictureTypeStandard,
                 max_letter='H',
                 max_number=8) -> None:
        self.type = board_type
        self.figure_positions = figure_positions
        self.max_letter = max_letter
        self.max_number = max_number
        self.all_cells = [Cell(i[0], int(i[1])) for i in product([chr(i) for i in range(ord('a'),
                                                                                        ord(
                                                                                            self.max_letter.lower()) + 1)],
                                                                 [str(i) for i in range(1, self.max_number + 1)])]
        self.board_picture = board_picture
        self.figure_path = "/chess_figures/merida/{}.png"

    @classmethod
    def get_json_from_positions(cls, positions: dict) -> str:
        # получаем json из словаря позиций
        return json.dumps({k: repr(v) for k, v in positions.items()})

    @classmethod
    def get_position_from_json(cls, pos: str) -> dict:
        # получаем позиции из json'a
        result = {}
        positions = json.loads(pos)
        for k, v in positions.items():
            try:
                value = json.loads(v)
            except json.decoder.JSONDecodeError:
                result[k] = standard_figures.get(v[1])(Cell(k[0], k[1]), v[0])
            else:
                if value.get("is_moved", None) is not None:
                    result[k] = standard_figures.get(value.get("type"))(Cell(k[0], k[1]),
                                                                        value.get("color"),
                                                                        value.get("is_moved") == "True")
                else:
                    result[k] = standard_figures.get(value.get("type"))(Cell(k[0], k[1]), value.get("color"))
        return result

    def get_picture(self):
        n = dt.now()
        figure_cache = {}
        i_util = Utils(self.board_picture.cell_size,
                       self.board_picture.lift_size_x,
                       self.board_picture.lift_size_y)
        board = i_util.get_image(self.board_picture.path)
        print("get board" + str(dt.now() - n))
        for k, v in self.figure_positions.items():
            figure = figure_cache.get(self.figure_path.format(v.get_str_for_file()))
            if figure is None:
                figure = i_util.get_image(self.figure_path.format(v.get_str_for_file()), need_resize=True)
                figure_cache[self.figure_path.format(v.get_str_for_file())] = figure
            print("get {} ".format(v) + str(dt.now() - n))
            i_util.set_position(board, figure, k)
            print("set_position {} ".format(v) + str(dt.now() - n))
        file = i_util.get_file_from_image(board)
        print("file " + str(dt.now() - n))
        return file

    def figure_delete(self, position: Cell) -> bool:
        # удаляем фигуру споля
        if self.figure_positions.get(position.get_position()) is not None:
            del self.figure_positions[position.get_position()]
            return True
        else:
            return False

    def figure_add(self, figure: AbstractFigure, position: Cell) -> bool:
        # ставим фигуру на поле
        if figure.can_move(position):
            figure.cell = position
            self.figure_positions[position.get_position()] = figure
            return True
        else:
            return False

    def get_figures_for_color(self, color: str) -> list:
        return [pos for pos, fig in self.figure_positions.items() if fig.color.lower() == color.lower()]

    def get_figure(self, position: Cell) -> AbstractFigure or None:
        figure = self.figure_positions.get(position.get_position())
        if figure is None:
            return None
        return figure

    def get_all_cells(self) -> List[Cell]:
        return self.all_cells
