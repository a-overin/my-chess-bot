class ChessException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class GameNotFoundException(ChessException):

    def __init__(self) -> None:
        super(GameNotFoundException, self).__init__("Game not found")


class GameSavePositionException(ChessException):

    def __init__(self) -> None:
        super().__init__("Error while save positions")


class FigureNotFoundException(ChessException):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
