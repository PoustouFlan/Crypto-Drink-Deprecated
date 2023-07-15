crypto_drink:
	cd src; python3 crypto_drink.py

clear_cache:
	rm -f src/data/db.sqlite3*
	rm src/data/tmp/*
