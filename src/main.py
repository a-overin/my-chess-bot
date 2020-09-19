import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence
from .commands import start, help_command, start_game, accept_game, error_handler, game_for_room, make_turn, set_start


def main():
    logging.debug('start')
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = os.environ.get('token')
    pp = PicklePersistence(filename='conversationbot')
    updater = Updater(token, use_context=True, persistence=pp)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    START, END = range(2)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("accept_game", accept_game),
                      CommandHandler("game", game_for_room)],
        states={
            START: [MessageHandler(Filters.regex('^[a-hA-H][1-8]$'), set_start)],

            END: [MessageHandler(Filters.regex('^[a-hA-H][1-8]$'), make_turn)]
        },
        fallbacks=[MessageHandler(Filters.regex('change start'), set_start)],
        name="game_conv",
        persistent=True,
        allow_reentry=True
    )

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("start_game", start_game))
    # dispatcher.add_handler(CommandHandler("accept_game", accept_game))
    # dispatcher.add_handler(CommandHandler("game", game_for_room))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, make_turn))
    dispatcher.add_handler(conv_handler)

    # on noncommand i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
