SHELL = /bin/sh

up:
	docker compose up --detach

up-build:
	docker compose up --build --detach

start:
	docker compose start

stop:
	docker compose stop

down:
	docker compose down

.PHONY: up up-build start stop down
