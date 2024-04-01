.PHONY: run
run:
	hledger bs -O csv | python3 ./get_currencies.py `hledger-get-default-currency`
