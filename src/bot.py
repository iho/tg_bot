import logging
import os

from telegram import (
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    bot,
)
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from utils import *

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

greeting_message = """
Welcome to Currency Exchange bot!
Use `/list` to get exchange data for USD.
Use `/exchange AMOUNT CURRENCY_1 CURRENCY_2` to get how much is AMOUNT of CURRENCY_1 worth in CURRENCY_2
e.g. `/exchange 100 USD UAH`
(default currencies are USD to GBP)
Use `/history CURRENCY_1/CURRENCY_2 7 days` to get graph of currencies relation for the data range
"""


def start_handler(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=greeting_message,
        parse_mode=ParseMode.MARKDOWN,
    )


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.start_polling()
    updater.idle()
