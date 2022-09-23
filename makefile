.PHONY: docs
docs:
	mkdocs serve

.PHONY: build
build:
	mkdocs build

.PHONY: deploy
deploy:
	mkdocs gh-deploy

.PHONY: dac
dac:
	python diagrams/dependencies.py
