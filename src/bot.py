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
def get_list_handler(update, context):
    currency = "USD"
    response = 'Some error happened. Sorry for inconvenience.'
    try:
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
    except Exception as e:
        logger.exception(e)

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response, parse_mode=ParseMode.MARKDOWN
    )


def start_handler(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=greeting_message,
        parse_mode=ParseMode.MARKDOWN,
    )


@typing
def exchange_handler(update, context):
    args = context.args
    if 'to' in args:
        args.remove('to')
    rates = None
    out = "USD"
    to = "GBP"
    amount = 0
    response = 'Some error happened. Sorry for inconvenience.'
    if len(args) == 3:
        amount, out, to = args
        amount = float(amount)
        out = out.upper()
        to = to.upper()
    elif len(args) == 2:
        # could fail if input is something like USD10
        out = args[0][0]  # first char of '$10' string
        amount = float(args[0][1:])
        to = args[-1].upper()
    else:
        response = 'Please, use `/exchange AMOUNT CURRENCY_1 CURRENCY_2` format.'
    try:
        rates = api.get_exchange_data(out, to)
    except Exception as e:
        logger.exception(e)
    if rates:
        total = amount * rates[to]
        response = f"{amount} {out} equals {total:.2f} {to}"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response,
        parse_mode=ParseMode.MARKDOWN
    )


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("list", get_list_handler))
    dispatcher.add_handler(CommandHandler("lst", get_list_handler))
    dispatcher.add_handler(CommandHandler('help', start_handler))
    dispatcher.add_handler(CommandHandler('exchange', exchange_handler))
    updater.start_polling()
    updater.idle()
