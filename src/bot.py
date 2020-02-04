import logging
import os
from datetime import datetime, timedelta

from pymongo import MongoClient
from telegram import (
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    bot,
)
from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

import api
from utils import *

rates_collection = MongoClient("localhost", 27017).currency_bot.rates_collection

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


@typing
def get_list(update, context):
    currency = "USD"
    previous_rates = rates_collection.find_one({"base": currency})
    now = datetime.now()
    if not previous_rates.get("date"):
        previous_rates["date"] = now
    if not previous_rates or (now + timedelta(minutes=10) >= previous_rates["date"]):
        rates = api.get_rates_data(currency)
        data = {"rates": rates, "date": datetime.now()}
        rates_collection.find_one_and_update(
            query={"base": currency}, update={"$set": data}, upsert=True
        )
    else:
        rates = previous_rates["rates"]

    response = "```\n"
    for (currency, price) in rates.items():
        response += f"{currency}: {price:.2f}\n"
    response += "\n```"

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.MARKDOWN
    )


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
    dispatcher.add_handler(CommandHandler("list", get_list))
    updater.start_polling()
    updater.idle()
