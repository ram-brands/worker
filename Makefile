.PHONY: getpoetry
get-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	poetry run pip3 install --upgrade pip
	poetry run poetry install

.PHONY: black
black:
	poetry run black app --check

.PHONY: black!
black!:
	poetry run black app

.PHONY: isort
isort:
	poetry run isort app --check

.PHONY: isort!
isort!:
	poetry run isort app

.PHONY: format!
format!: black! isort!

.PHONY: build
build:
	COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build
