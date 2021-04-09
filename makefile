docs:
	mkdocs serve

.PHONY: docs

build:
	mkdocs build

deploy:
	mkdocs gh-deploy