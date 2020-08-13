from ..figure.abstractFigure import AbstractFigure


class GameBoard:

    def __init__(self, board_type: int, figure_positions: dict, max_letter='H', max_number=8) -> None:
        self.type = board_type
        self.figure_positions = figure_positions
        self.max_letter = max_letter
        self.max_number = max_number

    @classmethod
    def get_json_from_positions(cls, positions: dict) -> str:
        # получаем json из словаря позиций
        pass

    @classmethod
    def get_position_from_json(cls, json: str) -> dict:
        # получаем позиции из json'a
        pass

    def figure_delete(self, position) -> bool:
        # удаляем фигуру споля
        pass

    def figure_add(self, figure: AbstractFigure) -> bool:
        # ставим фигуру на поле
        pass

