from .abstractGame import AbstractGame


class StandardGame(AbstractGame):
    def check_user_turn(self, user_id: int) -> bool:
        pass