import datetime


class UnsupportedTicker(ValueError):
    pass


def to_yahoo_ticker(ticker):
    CUSTOM_YAHOO_TICKER_TABLE = {
        "PLN": "PLNUSD=X",
        "EUR": "EURUSD=X",
        "CHF": "CHFUSD=X",
        "ETH": "ETH-USD",
    }

    EXCHANGE_CONVERSION_TABLE = {
        "XET": ".DE",
        "ARCA": "",
        "NYSE": "",
        "NDQ": "",
        "WSE": ".WA",
    }

    try:
        exchange, t = ticker.split(":")
        try:
            suffix = EXCHANGE_CONVERSION_TABLE[exchange]
        except KeyError:
            raise ValueError("no such exchange")
    except ValueError:  # nothing to split
        try:
            return CUSTOM_YAHOO_TICKER_TABLE[ticker]
        except KeyError:
            raise UnsupportedTicker(f"Ticker {ticker} is not explicitly supported")
    else:
        return f"{t}{suffix}"


def acquire_yahoo_quote(yahoo_ticker, requests_f) -> str:
    # TODO: use Session!
    q = f"https://query1.finance.yahoo.com/v8/finance/chart/{str(yahoo_ticker)}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
    h = {'User-Agent': 'twoj-stary/1.6.9', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    r = requests_f(q, headers=h)
    rj = r.json()
    try:
        price = rj["chart"]["result"][0]["meta"]["regularMarketPrice"]
        currency = rj["chart"]["result"][0]["meta"]["currency"]
    except TypeError:
        print("processing ", yahoo_ticker)
        raise
    return f"{price} {currency}"


def ble(c, requests_f) -> str:
    c_split = c.split(":")
    if len(c_split) != 2 or c_split[0] != "CRYPTO":
        raise UnsupportedTicker(f"{c} does not look like a cryptocurrency")
    _, token = c_split

    if token == "BIGSB" and datetime.datetime.now().date() < datetime.date(2025, 4, 1):
        # this token might be approaching 0, don't care that much about, may revisit at a later date or if I get other
        # niche crypto
        return "0.21 USD"

    raise UnsupportedTicker("Automation tbd")
    # https://www.coingecko.com/en/api
    # TODO: implement this
    # TODO: also implement secret passing, ugh


def main():
    import requests
    s = requests.Session()
    s.hooks = {
        'response': lambda r, *_args, **_kwargs: r.raise_for_status()
    }

    p = ble("CRYPTO:BIGSB", requests_f=s.get)
    print(p)


if __name__ == "__main__":
    main()
