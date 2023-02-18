# start the services
up:
	docker-compose up -d --build

# stop the services
down:
	docker-compose down

# restart the services
restart:
	docker-compose restart

# view the logs of the services
logs:
	docker-compose logs -f

# build the services
build:
	docker-compose build

# stop and remove all containers, volumes, and networks
clean:
	docker-compose down --volumes --remove-orphans

# run the services in the foreground
runserver: up
	docker-compose exec server python manage.py runserver 0.0.0.0:9000

migrations: up
	docker-compose exec server python manage.py makemigrations

migrate: up
	docker-compose exec server python manage.py migrate

command: up
	docker-compose exec server $(filter-out $@,$(MAKECMDGOALS))

.PHONY: up down restart logs build run clean runserver migrate migrations
