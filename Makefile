test: ## Запуск контейнера с тестом с отдельной БД
	docker compose -f docker-compose.test.yml up -d
app:  ## Запуск контейнера с приложением
	docker compose up -d
