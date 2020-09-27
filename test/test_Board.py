from src.game.gameMaker import GameMaker
from src.game.board.boardCell import Cell
from datetime import datetime as dt
from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from itertools import groupby

chat_id = -463741226

n = dt.now()

maker = GameMaker()
game = maker.get_game_for_chat_room(chat_id)
# pic = game.board.get_picture()
# with open("test.png", "wb") as f:
#     f.write(pic.getvalue())
# print(dt.now() - n)
dat = game.get_available_for_position(Cell('c', 1))
res = groupby(dat, lambda x: x[0])
for k, g in res:
    print(k)
    print([i for i in g])
