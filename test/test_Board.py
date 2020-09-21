from src.game.gameMaker import GameMaker
from src.game.board.boardCell import Cell
from datetime import datetime as dt
from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton

chat_id = -463741226

n = dt.now()

maker = GameMaker()
game = maker.get_game_for_chat_room(chat_id)
# pic = game.board.get_picture()
# with open("test.png", "wb") as f:
#     f.write(pic.getvalue())
# print(dt.now() - n)
dat = game.get_available_for_position(Cell('c', 1))
print(dat)
buttons = [KeyboardButton(pos) for pos in dat]
print(buttons)
markup = ReplyKeyboardMarkup.from_row(buttons,
                                      resize_keyboard=False,
                                      selective=True,
                                      one_time_keyboard=True)
print(markup)
