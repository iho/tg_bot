import requests


def get_rate_data(currency="USD"):
    data = requests.get(
        url=f"https://api.exchangeratesapi.io/latest?base={currency}"
    ).json()
    return data["rates"]


# handler for exchange data args
def get_exchange_data(out="USD", to="GBP", amount=1):
    out = check_if_symbol(out)
    to = check_if_symbol(to)
    response = requests.get(
        f"https://api.exchangeratesapi.io/latest?symbols={to}&base={out}"
    )
    if response.get("error", None):
        return response["error"]
    response = amount * response["rates"][to]
    return f"{amount} {out} equals {response:.2f} {to}"


def format_date(date):
    return date.strftime("%Y-%m-%d")
