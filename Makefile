SHELL := /bin/bash

init:
	pip install -r requirements.test.txt

test:
	rm -f .coverage
	python3 -m pytest --cov=src/tomatinho

install:
	sudo python3 setup.py install --install-layout=deb

.PHONY: all test clean
