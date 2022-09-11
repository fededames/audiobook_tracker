REFORMAT_DIRS=app/

.PHONY: fmt
fmt:
	@echo "\n=> Formating files..."
	black $(REFORMAT_DIRS)
	isort $(REFORMAT_DIRS)
	flake8 --ignore E501,E203,E731,W503 $(REFORMAT_DIRS)

.PHONY: test
test: fmt
	docker-compose run --rm app sh -c "python manage.py wait_for_db && pytest"