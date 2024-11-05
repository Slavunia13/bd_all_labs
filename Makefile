run:  ##@Run app
	docker compose -f docker-compose.yml up --remove-orphans

build:  ##@Build app and database
	docker compose -f docker-compose.yml build

env: ##@Generate env file
	cp .env.example .env

