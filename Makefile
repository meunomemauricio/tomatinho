SHELL := /bin/bash

init:
	pip install -r requirements.test.txt

test:
	rm .coverage
	pytest --cov=src/tomatinho

.PHONY: all test clean
