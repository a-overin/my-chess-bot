import logging
import os
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from .commands import start, help_command, start_game, accept_game, error_handler,\
    game_for_room, make_turn, set_start, change_piece
from .persist import MyPersistence
from chess import UNICODE_PIECE_SYMBOLS, SAN_REGEX


def main():
    logging.debug('start')
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = os.environ.get('token')
    persist = MyPersistence()
    updater = Updater(token, use_context=True, persistence=persist)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    SAN_REGEX = re.compile(r"^(O?(\-O){1,2}[\+#]?)?(([NBKRQ])?([a-h])?([1-8])?[\-x]?([a-h][1-8])(=?[nbrqkNBRQK])?[\+#]?)?\Z")
    start_conv, end_conv = range(2)
    unicode_figures = "|".join([fig for fig in UNICODE_PIECE_SYMBOLS.values()])
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("accept_game", accept_game),
                      CommandHandler("game", game_for_room)],
        states={
            start_conv: [MessageHandler(Filters.regex('^('+unicode_figures+')$'), set_start)],

            end_conv: [MessageHandler(Filters.regex(SAN_REGEX), make_turn)]
        },
        fallbacks=[MessageHandler(Filters.regex('Change piece'), change_piece)],
        name="game_conv",
        persistent=True,
        allow_reentry=True
    )

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
