class GameNotFoundException(Exception):

    def __init__(self) -> None:
        super(GameNotFoundException, self).__init__("Game not found")


class GameSavePositionException(Exception):

    def __init__(self) -> None:
        super().__init__("Error while save positions")
