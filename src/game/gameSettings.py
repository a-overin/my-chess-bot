class GameType:
    @staticmethod
    def standard():
        return 1


class GameStatuses:
    @classmethod
    def created(cls):
        return 0

    @classmethod
    def started(cls):
        return 5

    @classmethod
    def draw(cls):
        return 10

    @classmethod
    def white_win(cls):
        return 15

    @classmethod
    def black_win(cls):
        return 20