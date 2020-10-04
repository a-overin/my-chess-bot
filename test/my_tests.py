from game.board.gameBoard import GameBoard
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
pic = game.board.get_picture()
