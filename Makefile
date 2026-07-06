.PHONY: build up down logs shell test clean rebuild

IMAGE ?= binder-launcher
SERVICE ?= launcher
PORT ?= 8888

run: up


build:
	docker compose build --no-cache

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f $(SERVICE)

shell:
	docker compose run --rm --service-ports $(SERVICE) bash

test:
	@echo "Open:"
	@echo "http://localhost:$(PORT)/launch?repo=$(TEST_REPO)&branch=$(TEST_BRANCH)&notebookpath=$(TEST_NOTEBOOK)"

curl-test:
	curl -v "http://localhost:$(PORT)/launch?repo=$(TEST_REPO)&branch=$(TEST_BRANCH)&notebookpath=$(TEST_NOTEBOOK)"

rebuild:
	docker compose down
	docker compose build --no-cache
	docker compose up

clean:
	docker compose down --volumes --remove-orphans
	docker image rm $(IMAGE) 2>/dev/null || true
