import requests

import symbols


def get_rates_data(currency="USD"):
    data = requests.get(
        url=f"https://api.exchangeratesapi.io/latest?base={currency}"
    ).json()
    return data["rates"]


def _check_if_symbol(currency):
    return symbols.symbols.get(currency, currency)


def get_exchange_data(out, to):
    out = _check_if_symbol(out)
    to = _check_if_symbol(to)
    response = requests.get(
        f"https://api.exchangeratesapi.io/latest?symbols={to}&base={out}"
    )

    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    return response.json()["rates"]


def format_date(date):
    return date.strftime("%Y-%m-%d")
