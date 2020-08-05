def start(update, context):
    update.message.reply_text('Hi!')


def help_command(update, context):
    update.message.reply_text('help!')


def echo(update, context):
    update.message.reply_text(update.message.text)
