import csv
import datetime
import sys

import requests

from acquire_quote import acquire_yahoo_quote, to_yahoo_ticker, UnsupportedTicker, ble

# let me know if this changes
GLOBAL_RESERVE_CURRENCY = "USD"

def main():
    # TODO: call hledger directly
    raw_data = sys.stdin.readlines()

    *_, net = csv.reader(raw_data)
    assert net[0] == "Net:"
    currencies_with_ammounts = net[1].split(",")

    # TODO: simplfy this and move exclusion logic to different function
    currencies = set()
    for amount in currencies_with_ammounts:
        curency = (amount.lstrip().split(" ")[1]).strip('"')

        # Use OTC: to designate no price fetching for this currency
        # since it's not being offered on the open market
        if curency.startswith("OTC:"):
            continue

        # this is an 2024 February experiment with counting bills directly
        if curency.startswith("PLN:"):
            continue
        
        currencies.add(curency)

    # 31/08/2023: for some time now LEV has a fixed exchange rate with EUR, so 
    # you only have to input it once
    # P 2023/08/31 EUR 1.95583 LEV
    # feel free to implement fancy checking if LEV is desired and if the price is indeed in the ledger
    # ^ otherwise include the price in the final output
    # also: feel free to find out the exact date for setting the peg
    # TODO: actually this check might be also usefull for OTC when doing a new ledger
    currencies.discard("LEV")  

    # TODO: make a workaround for default currency to use global reserve currency as a fallback
    default_currency = sys.argv[1]
    desired_currencies = currencies

    today = str(datetime.datetime.now().date()).replace("-", "/")
    s = requests.Session()
    s.hooks = { 'response': lambda r, *_args, **_kwargs: r.raise_for_status() }

    for c in desired_currencies:
        # TODO: refactor the error handling
        # TODO: potentially async this, the order doesn't matter
        try:
            p = acquire_yahoo_quote(to_yahoo_ticker(c), requests_f=s.get)
        except UnsupportedTicker:
            try:
                p = ble(c, requests_f=s.get)
            except UnsupportedTicker:
                p = f"!_WPISZ_TUTAJ_CENĘ_! {default_currency}"

        print(f"P {today} {c} {p}")


if __name__ == "__main__":
    main()
