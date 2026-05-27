.PHONY: demo build up down clean

demo: build up

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Demo is starting... Open http://localhost:8501"

down:
	docker-compose down

clean:
	docker-compose down -v --rmi all
	rm -rf data/*
