import sys
import csv
import functools
import datetime

from acquire_quote import to_yahoo_ticker, acquire_yahoo_quote


GLOBAL_RESERVE_CURRENCY = "USD"
HARDCODED = {GLOBAL_RESERVE_CURRENCY}

def main():
    raw_data = sys.stdin.readlines()

    for line in raw_data:
        if "Net:" in line:
            the_line = line
            break
    else:
        raise RuntimeError("Couldn't find Net:")

    currencies_info = the_line.split('"')[3]
    currency_amounts = currencies_info.split(",")
    currencies = set()
    for amount in currency_amounts:
        currencies.add((amount.lstrip().split(" ")[1]))

    # 31/08/2023: for some time now LEV has a fixed exchange rate with EUR, so 
    # you only have to input it once
    currencies.disacard("LEV")  

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
