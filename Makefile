include .env

all: build

build:
	docker compose up --build