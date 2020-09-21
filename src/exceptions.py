class ChessException(Exception):

    pass


class GameNotFoundException(ChessException):

    def __init__(self) -> None:
        super().__init__("Game not found")


class GameSavePositionException(ChessException):

    def __init__(self) -> None:
        super().__init__("Error while save positions")


class FigureNotFoundException(ChessException):

    pass
