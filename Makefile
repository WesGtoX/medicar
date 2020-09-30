build:
	docker-compose -f backend/docker-compose.yml build

bash:
	docker-compose -f backend/docker-compose.yml run --rm api bash

run:
	docker-compose -f backend/docker-compose.yml up

test:
	docker-compose -f backend/docker-compose.yml run --rm api pytest

down:
	docker-compose -f backend/docker-compose.yml down -v
