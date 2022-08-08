local_uvicorn:
	uvicorn raspberries.adapters.api:app --proxy-headers --host 0.0.0.0 --port 8000

up:
	docker-compose up --build

down:
	docker-compose down

pip-tools:
	pip install pip-tools

compile-reqs: pip-tools
	pip-compile requirements.in
	pip-compile requirements-dev.in

reqs: compile-reqs
	pip-sync requirements-dev.txt

install:
	poetry run python -m pip install pip==21.1.3
	poetry install

prepare:
	isort app/

mypy:
	mypy app/

flake:
	flake8 app/

test:
	pytest -vvv -n auto --cov-config=.coveragerc --cov=./raspberries --cov-fail-under=90

check: mypy flake test
	@echo "Ok"