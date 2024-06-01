CUSTOM_YAHOO_TICKER_TABLE = {
    "PLN": "PLNUSD=X",
    "EUR": "EURUSD=X",
    "ETH": "ETH-USD",
}

EXCHANGE_CONVERSION_TABLE = {
    "XET": ".DE",
    "NYSEARCA": "",
    "NYSE": "",
    "NDQ": "",
    "WSE": ".WA",
}

def main():
    import requests
    p = acquire_yahoo_quote("DAX.DE", requests_f=requests)
    print(p)


def to_yahoo_ticker(ticker):
    try:
        exchange, t = ticker.split(":")
        try:
            suffix = EXCHANGE_CONVERSION_TABLE[exchange]
        except KeyError:
            raise ValueError("no such exchange")
    except ValueError:
        return CUSTOM_YAHOO_TICKER_TABLE[ticker]
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


if __name__ == "__main__":
    main()
