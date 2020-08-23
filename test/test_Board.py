from src.game.gameMaker import GameMaker
from datetime import datetime as dt

chat_id = -463741226

n = dt.now()

maker = GameMaker()
game = maker.get_game_for_chat_room(chat_id)
pic = game.board.get_picture()
with open("test.png", "wb") as f:
    f.write(pic.getvalue())
print(dt.now() - n)
