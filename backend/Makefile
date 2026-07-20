.PHONY: install dev test benchmark profile load-test

install:
	pip install -r requirements.txt
	cd frontend && npm install

dev:
	docker-compose up --build

test:
	pytest backend/tests/ backend/benchmarks/
	cd frontend && npm test

benchmark:
	pytest backend/benchmarks/ --benchmark-only --benchmark-json=benchmarks.json

profile:
	python -m cProfile -o profile_stats.prof backend/main.py

load-test:
	locust -f backend/benchmarks/load_testing/locustfile.py