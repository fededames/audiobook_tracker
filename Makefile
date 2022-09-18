REFORMAT_DIRS=app/

.PHONY: fmt
fmt:
	@echo "\n=> Formating files..."
	black $(REFORMAT_DIRS)
	isort $(REFORMAT_DIRS)
	flake8 --ignore E501,E203,E731,W503 $(REFORMAT_DIRS)

PHONY: postgres
postgres:
	@echo "\n=> Starting Postgres..."
	docker run \
	--rm \
	--name postgres \
	-e POSTGRES_USER=devuser \
	-e POSTGRES_PASSWORD=changeme \
	-e POSTGRES_DB=devdb \
	-p 5432:5432 \
	postgres:13-alpine

PHONY: migrations
migrations:
	python app/manage.py migrate

.PHONY: test
test: fmt
	docker-compose run --rm app sh -c "python manage.py wait_for_db && pytest"

# With docker compose already up
PHONY: backup_db
backup_db:
	docker exec audiobook_tracker_db_1  pg_dump -U devuser -Fc devdb > db.dump

PHONY: restore_db
restore_db:
	docker exec -i audiobook_tracker_db_1  pg_restore -U devuser -C -d postgres < db.dump


.PHONY: get_best_sellers
get_bestsellers:
	docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py get_bestsellers"