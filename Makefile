.PHONY: install dev test

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

dev:
	docker-compose up --build

test:
	pytest backend/tests/
	cd frontend && npm test