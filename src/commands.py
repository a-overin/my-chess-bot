import html
import json
import logging
import os
import traceback
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from .game.gameMaker import GameMaker
from .user.user_service import UserService

logger = logging.getLogger(__name__)

DEVELOPER_CHAT_ID = os.environ.get('developer_chat_id')


# Здесь описываем команды
def start(update: Update, context: CallbackContext):
    service = UserService()
    text = "Service unavailable"
    try:
        if service.check_user(update.message.from_user.id):
            text = "Welcome, you are registered!"
        else:
            text = "Sorry, you are not registered!"
    except Exception as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=text)
        raise
    else:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=text)


def help_command(update: Update, context: CallbackContext):
    service = UserService()
    if service.check_user(update.message.from_user.id):
        text = "Information: " + str(service.get_user(update.message.from_user.id))
    else:
        text = "Sorry, you are not registered!"
    context.bot.send_message(chat_id=update.message.chat.id,
                             text=text)


def game_for_room(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.get_game_for_chat_room(update.message.chat.id)
    except Exception as error:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        context.bot.send_photo(chat_id=update.message.chat.id,
                               caption="Game for room",
                               photo=game.board.get_picture()
                               )


def start_game(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.create_game(update.message.chat.id, update.message.from_user.id)
    except Exception as error:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 reply_to_message_id=update.message.message_id,
                                 text="Game created, id = " + str(game.id))


def accept_game(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.accept_game(update.message.chat.id, update.message.from_user.id)
    except Exception as error:
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        context.bot.send_photo(chat_id=update.message.chat.id,
                               caption="Game successfully accepted",
                               photo=game.board.get_picture()
                               )


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_str = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb_str)
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
