def start(update):
    update.message.reply_text('Hi!')


def help_command(update):
    update.message.reply_text('help!')


def echo(update):
    update.message.reply_text(update.message.text)
