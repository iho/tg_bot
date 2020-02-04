from functools import wraps

import matplotlib.pyplot as plt
from telegram import ChatAction


def create_graph(data, out, to, start, finish, filepath):
    print(data)
    x_values = [date for date, values in data.items()]
    y_values = [float(values[out]) for date, values in data.items()]

    plt.plot(x_values, y_values, label=f"{out} to {to}")

    for x, y in zip(x_values, y_values):
        label = f"{y:.4f}"
        plt.annotate(
            label, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    plt.xlabel(f"Dates")
    plt.ylabel(f"1 {out} in {to}")
    plt.title(f"{out} to {to} relation in dates from {start} to {finish}")
    plt.legend()
    plt.tight_layout()
    x1, x2, y1, y2 = plt.axis()
    # 0.0005 could look even better
    plt.axis((x1, x2, y1 - 0.001, y2 + 0.001))
    plt.savefig(filepath, format="png")
    plt.close()


def typing(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return wrapped


def uploading(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.UPLOAD_PHOTO
        )
        return func(update, context, *args, **kwargs)

    return wrapped


def format_date(date):
    return date.strftime("%Y-%m-%d")
