import numpy
from game.board.gameBoard import GameBoard
from src.game.gameDao import GameDao
from src.game.gameMaker import GameMaker
from datetime import datetime as dt
from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton
from itertools import groupby
from chess import Board, Move
from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton
chat_id = -463741226


# unicode_figures = [fig.encode("utf-8").decode("utf-8") for fig in chess.UNICODE_PIECE_SYMBOLS.values()]
# print(len(unicode_figures))
# res = [i.tolist() for i in numpy.array_split(unicode_figures, len(unicode_figures)//4 + 1)]
# print(res + [["asd"]])

board = Board()
board.push_san("d4")
print(board.unicode())
print(board.variation_san(board.move_stack))

