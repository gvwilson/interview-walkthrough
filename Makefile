all: commands

## commands: show available commands (*)
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: rebuild docs
build:
	python picossg.py --src src --dst docs --templates templates

## serve: serve the docs
serve:
	python -m http.server -d docs 8000

## clean: clean up
clean:
	@rm -rf dist docs mccole.egg-info
	@find . -type f -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
	@find . -type d -name .pytest_cache | xargs rm -r
	@find . -type d -name .ruff_cache | xargs rm -r
