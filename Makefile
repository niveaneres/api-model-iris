SHELL := /bin/bash
PROJECT_NAME = api-iris-model
DOCKER_IMG := $(PROJECT_NAME):latest
SERVICE_PORT := 9002

help:
	@echo "usage: make <command> [VERSION=X.Y.Z]"
	@echo
	@echo "COMMANDS"   
	@echo "    help     Show this help"
	@echo "    format   Using black before commit to style code"
	@echo "    flake    Using Flake8"
	@echo "    mypy     Using mypy"
	@echo "    build    Build docker image from Dockerfile"
	@echo "    run    	Build and run the docker image"
	@echo "    clean    Stop and remove the docker image"


run-local:
	flask --app app run

build:
	docker build -t $(PROJECT_NAME) .

run:build
	docker run --name $(PROJECT_NAME) -d -p $(SERVICE_PORT):8080 $(DOCKER_IMG)

stop:
	docker stop $(PROJECT_NAME)

clean:
	docker stop $(PROJECT_NAME)
	docker rm $(PROJECT_NAME)
	docker volume rm $(DOCKER_IMG) --force


flake:
	pip install flake8
	flake8 app.py
	flake8 lmodel/

	mypy:
	pip install --no-cache-dir mypy==0.931
	mypy --cache-dir=/dev/null --ignore-missing-imports app.py
	mypy --cache-dir=/dev/null --ignore-missing-imports lmodel/

format:
	pip install black
	black app.py
	black lmodel/


test:
	pytest ./tests