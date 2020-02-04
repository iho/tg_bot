from functools import wraps

import matplotlib.pyplot as plt


def create_graph(data, out, to, start, finish, filepath):
    # unpack X and Y values - dates and amounts
    print(data)
    x_values = list(data["rates"].keys())
    y_values = [float(values[out]) for values in data["rates"].values()]

    # build a generic plot
    plt.plot(x_values, y_values, label=f"{out} to {to}")

    # add labels to all plot points
    for x, y in zip(x_values, y_values):
        label = f"{y:.4f}"
        plt.annotate(
            label, (x, y), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    plt.xlabel(f"Dates")
    plt.ylabel(f"1 {out} in {to}")
    plt.title(f"{out} to {to} relation in dates from {start} to {finish}")
    plt.legend()
    # fix margins
    plt.tight_layout()
    x1, x2, y1, y2 = plt.axis()
    # 0.0005 could look even better
    plt.axis((x1, x2, y1 - 0.001, y2 + 0.001))
    plt.savefig(filepath)


# typing status wrapper
def typing(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return wrapped
