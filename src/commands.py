from telegram import Update
from .game.gameMaker import GameMaker


# Здесь описываем команды
def start(update: Update):
    update.message.reply_text('Hi!')


def help_command(update: Update):
    update.message.reply_text('help!')


def echo(update: Update):
    update.message.reply_text(update.message.text)


def start_game(update: Update):
    game_maker = GameMaker()
    game_maker.get_game_for_chat_room(update.message.chat.id)
