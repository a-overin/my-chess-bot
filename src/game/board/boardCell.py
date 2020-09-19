class Cell:
    def __init__(self, letter: str, number: int) -> None:
        # буква клетки
        self.letter = letter.lower()
        # номер клетки
        self.number = number

    def get_position(self) -> str:
        return self.letter + str(self.number)

    @classmethod
    def from_str(cls, pos: str):
        return Cell(pos[0], int(pos[1]))

    def __str__(self) -> str:
        return self.letter.upper() + str(self.number)

    def __repr__(self) -> str:
        return self.letter.upper() + str(self.number)


