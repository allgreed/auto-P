import sys
import csv
import functools
import datetime

from acquire_quote import to_yahoo_ticker, acquire_yahoo_quote


GLOBAL_RESERVE_CURRENCY = "USD"
HARDCODED = {GLOBAL_RESERVE_CURRENCY}

def main():
    raw_data = sys.stdin.readlines()

    *_, net = csv.reader(raw_data)
    assert net[0] == "Net:"

    currencies_with_ammounts = net[1].split(",")
    currencies = set()
    for amount in currencies_with_ammounts:
        currencies.add((amount.lstrip().split(" ")[1]))

    # 31/08/2023: for some time now LEV has a fixed exchange rate with EUR, so 
    # you only have to input it once
    # P 2023/08/31 EUR 1.95583 LEV
    currencies.discard("LEV")  

    default_currency = sys.argv[1]
    desired_currencies = currencies.union(HARDCODED).difference({GLOBAL_RESERVE_CURRENCY})

    today = str(datetime.datetime.now().date()).replace("-", "/")
    for c in desired_currencies:
        try:
            p = acquire_yahoo_quote(to_yahoo_ticker(c))
        except KeyError:
            p = f"!_WPISZ_TUTAJ_CENĘ_! {GLOBAL_RESERVE_CURRENCY}"

        print(f"P {today} {c} {p}")


if __name__ == "__main__":
    main()
