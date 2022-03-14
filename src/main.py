from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from typing import Final

import pathlib
import logging
import image_util
import imghdr

ukrainian_flag: Final[str] = "./resources/ukrainian_flag.png"
payment_infos: Final[str] = "./resources/payment.txt"

logging.basicConfig(filename="bot.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

with open(payment_infos, 'r') as payment_file:
    payment_infos = payment_file.read()


def get_biggest_image(update: Update, context: CallbackContext, path_to_save: str):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download(path_to_save)


def start(update: Update, _):
    update.message.reply_text(
        "Send your image and the bot will add ukrainian flag to it.\n" +
        "Надішліть своє зображення і бот додасть до нього український прапор."
    )


def get_overlay_path(update: Update):
    chat_id = update.effective_chat.id
    overlay_path = f"./resources/overlay{chat_id}.jpg"
    output_path = f"./resources/output{chat_id}.jpg"
    return overlay_path, output_path, chat_id


def uaficy_doc(update: Update, context: CallbackContext):
    overlay_path, output_path, chat_id = get_overlay_path(update)
    context.bot.get_file(update.message.document).download(overlay_path)
    if imghdr.what(overlay_path) is None:
        update.message.reply_text("File type is not supported!")
    uaficy(update, context, overlay_path, output_path, chat_id)


def uaficy_img(update: Update, context: CallbackContext):
    logging.info(update.effective_chat)
    overlay_path, output_path, chat_id = get_overlay_path(update)
    get_biggest_image(update, context, overlay_path)


def uaficy(update, context, overlay_path, output_path, chat_id):
    try:
        image_util.add_background(ukrainian_flag,
                                  overlay_path,
                                  output_path)
        context.bot.send_document(chat_id=chat_id, document=open(output_path, 'rb'))

        update.message.reply_text("It will help also if you will support Ukraine!")
        update.message.reply_text(payment_infos)
    finally:
        pathlib.Path(overlay_path).unlink(missing_ok=True)
        pathlib.Path(output_path).unlink(missing_ok=True)


def unknown(update: Update, _):
    update.message.reply_text(
        f"Sorry {update.message.text} is not a valid command.\n"
        f"На жаль, {update.message.text} недійсна команда")


with open('./key.telegram', 'rt') as key_file:
    key = key_file.read()
    updater = Updater(key, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, uaficy_img))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, uaficy_doc))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.command, unknown))  # Filters out unknown commands

    updater.start_polling()
