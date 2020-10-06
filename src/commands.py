import html
import json
import logging
import os
import traceback
import numpy
from telegram import Update, ParseMode, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import CallbackContext

from .game.abstractGame import AbstractGame
from .exceptions import ChessException
from .game.gameMaker import GameMaker
from .user.user_service import UserService

logger = logging.getLogger(__name__)

DEVELOPER_CHAT_ID = os.environ.get('developer_chat_id')
START, END = range(2)


# Здесь описываем команды
def start(update: Update, context: CallbackContext):
    service = UserService()
    text = "Service unavailable"
    try:
        if service.check_user(update.message.from_user.id):
            text = "Welcome, you are registered!"
        else:
            text = "Sorry, you are not registered!"
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    except Exception as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=text)
        raise error
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
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        text, markup = get_message_for_room(game, context, update)
        context.bot.send_photo(chat_id=update.message.chat.id,
                               caption=text,
                               photo=game.board.get_picture(),
                               reply_markup=markup
                               )
        return START


def set_start(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game: AbstractGame = game_maker.get_game_for_chat_room(update.message.chat.id)
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        if game.check_user_turn(update.message.from_user.id):
            figure = update.message.text
            context.chat_data['figure'] = figure
            markup = make_keyboard(game.get_available_for_figure(figure=figure), True)
            logger.info(context.chat_data.get("mess_id"))
            context.bot.send_message(chat_id=update.message.chat.id,
                                     text="select turn",
                                     reply_to_message_id=update.message.message_id,
                                     reply_markup=markup
                                     )
        else:
            return START
    return END


def make_turn(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.get_game_for_chat_room(update.message.chat.id)
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        if game.check_user_turn(update.message.from_user.id):
            turn = update.message.text
            game.make_turn(update.message.from_user.id, turn)
            if game.board.board.is_game_over():
                color, text = game.get_results()
                game_maker.update_rating(update.message.chat.id, color)
                markup = ReplyKeyboardRemove()
            else:
                game = game_maker.get_game_for_chat_room(update.message.chat.id)
                text, markup = get_message_for_room(game, context, update)
            context.bot.send_photo(chat_id=update.message.chat.id,
                                   caption=text,
                                   photo=game.board.get_picture(),
                                   reply_markup=markup
                                   )
    return START


def start_game(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.create_game(update.message.chat.id, update.message.from_user.id)
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
    else:
        text = "Game created, id = " + str(game.id) + "\n Someone need /accept_game"
        context.bot.send_message(chat_id=update.message.chat.id,
                                 reply_to_message_id=update.message.message_id,
                                 text=text)


def accept_game(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.accept_game(update.message.chat.id, update.message.from_user.id)
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
        raise
    else:
        text, markup = get_message_for_room(game, context, update)
        m_id = context.bot.send_photo(chat_id=update.message.chat.id,
                                      caption="Game successfully accepted\n" + text,
                                      photo=game.board.get_picture(),
                                      reply_markup=markup
                                      ).message_id
        context.chat_data["mess_id"] = m_id
        return START


def change_piece(update: Update, context: CallbackContext):
    try:
        game_maker = GameMaker()
        game = game_maker.get_game_for_chat_room(update.message.chat.id)
        markup = make_keyboard(game.get_figures_for_move())
    except ChessException as error:
        logger.error(error)
        context.bot.send_message(chat_id=update.message.chat.id,
                                 text=str(error))
        raise
    context.bot.send_message(chat_id=update.message.chat.id,
                             text="Change piece",
                             reply_to_message_id=update.message.message_id,
                             reply_markup=markup)
    return START


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


def get_message_for_room(game, context, update):
    user = context.bot.get_chat_member(update.message.chat.id, game.user_turn).user
    text = "Game id {}, turn number {}, wait user {}".format(game.id, game.turn_number, user.name)
    text = text + "\nLast move: " + game.board.get_last_move() if game.board.get_last_move() != "" else text
    markup = make_keyboard(game.get_figures_for_move())
    return text, markup


def make_keyboard(rows: set, fl_need_back: bool = False) -> ReplyKeyboardMarkup:
    grouped = grouper(rows, 5)
    buttons = []
    for row in grouped:
        buttons.append([KeyboardButton(cell) for cell in row])
    if fl_need_back:
        buttons.append([KeyboardButton("Change piece")])
        markup = ReplyKeyboardMarkup(buttons,
                                     resize_keyboard=True,
                                     selective=True,
                                     one_time_keyboard=True)
    else:
        markup = ReplyKeyboardMarkup(buttons,
                                     resize_keyboard=True,
                                     selective=True,
                                     one_time_keyboard=True)
    return markup


def grouper(iterable, n):
    return [i.tolist() for i in numpy.array_split(list(iterable), len(iterable)//n + 1)]
