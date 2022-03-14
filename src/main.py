from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import pathlib
from typing import Final

import image_util

ukrainian_flag: Final[str] = "./resources/ukrainian_flag.png"


def get_biggest_image(update: Update, context: CallbackContext, path_to_save: str):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download(path_to_save)


def start(update: Update, _):
    update.message.reply_text(
        "Enter the text you want to show to the user whenever they start the bot")


def uaficy(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    overlay_path = f"./resources/overlay{chat_id}.jpg"
    output_path = f"./resources/output{chat_id}.jpg"
    try:
        get_biggest_image(update, context, overlay_path)
        image_util.add_background(ukrainian_flag,
                                  overlay_path,
                                  output_path)
        context.bot.send_document(chat_id=chat_id, document=open(output_path, 'rb'))
    finally:
        pathlib.Path(overlay_path).unlink(missing_ok=True)
        pathlib.Path(output_path).unlink(missing_ok=True)


def unknown(update: Update, _):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


with open('./key.telegram', 'rt') as key_file:
    key = key_file.read()
    updater = Updater(key, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, uaficy))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown))  # Filters out unknown commands

    updater.start_polling()
