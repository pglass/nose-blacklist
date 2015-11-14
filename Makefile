
test: lint
	nosetests -v --processes=2 --logging-level=INFO tests/*.py

lint:
	flake8 noseblacklist/ tests/
