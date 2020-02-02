import logging
import os
import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from beatnik_api import get_beatnik_data


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TOKEN = os.environ['TELEGRAM_TOKEN']
MESSAGE_FORMAT_STRING = """
*{title}*
*{artist}*
*{album}*

"""

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def convert(update, context):
    # remove "/convert" from the string
    user_string = update.message.text[8:].strip()

    if len(user_string) < 1:
        return

    beatnik_data = get_beatnik_data(user_string)
    if len(beatnik_data['errors']) > 0:
        for error in beatnik_data['errors']:
            logger.warning("Beatnik API returned an error:" + str(error))

    message = format_message(beatnik_data)
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=beatnik_data['album_art'],
        caption=message,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def format_message(beatnik_data):
    message = MESSAGE_FORMAT_STRING.format(
        title=beatnik_data['title'],
        artist=beatnik_data['artist'],
        album=beatnik_data['album'],)

    if not beatnik_data["apple"] is None:
        message += "[Apple Music]({})\n".format(beatnik_data["apple"])

    if not beatnik_data["gpm"] is None:
        message += "[Google Music]({})\n".format(beatnik_data["gpm"])

    if not beatnik_data["spotify"] is None:
        message += "[Spotify]({})\n".format(beatnik_data["spotify"])

    if not beatnik_data["soundcloud"] is None:
        message += "[Soundcloud]({})\n".format(beatnik_data["soundcloud"])

    return message


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("convert", convert))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
