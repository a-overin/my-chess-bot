import os
import requests
from io import BytesIO
from PIL import Image


class Utils:

    def __init__(self, cell_size: int = 81, board_size_x: int = 53, board_size_y: int = 55) -> None:
        self._image_host = os.environ.get("CLOUDCUBE_URL") + "/public"
        self._cell_size = cell_size
        self._border_size_x = board_size_x
        self._border_size_y = board_size_y

    def get_image(self, path: str):
        board_path = self._image_host + path
        response = requests.get(board_path)
        image = Image.open(BytesIO(response.content)).convert("RGBA")
        return image

    def set_position(self, board, figure, position: str):
        x = self.__get_x_from_letter(position[0].lower())
        y = self.__get_y_from_numb(int(position[1]))
        board.paste(figure, (x, board.size[1] - y), figure)

    @staticmethod
    def get_file_from_image(image):
        bio = BytesIO()
        bio.name = "board.png"
        image.save(bio, 'PNG')
        bio.seek(0)
        return bio

    def __get_y_from_numb(self, number: int) -> int:
        return self._border_size_y + self._cell_size * number

    def __get_x_from_letter(self, letter: str) -> int:
        coefficient = 0
        if letter == 'a':
            coefficient = 0
        elif letter == 'b':
            coefficient = 1
        elif letter == 'c':
            coefficient = 2
        elif letter == 'd':
            coefficient = 3
        elif letter == 'e':
            coefficient = 4
        elif letter == 'f':
            coefficient = 5
        elif letter == 'g':
            coefficient = 6
        elif letter == 'h':
            coefficient = 7
        return self._border_size_x + self._cell_size * coefficient
