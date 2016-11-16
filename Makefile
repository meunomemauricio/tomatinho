SHELL := /bin/bash

init:
	pip install -r requirements.test.txt

test:
	rm -f .coverage
	python3 -m pytest --cov=src/tomatinho

.PHONY: all test clean
