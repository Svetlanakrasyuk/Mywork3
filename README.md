# Mywork3
Проект создан на FastAPI с использованием PostgreSQL в качестве БД и Redis для кеширования данных.
Работа с базой и кеширование вынесены в отдельные слои.

Для запуска проекта необходимо:
1. Скачать проект с github
2. Извлечь файлы в папку проекта.
3. Для запуска основного приложения make app или docker compose up -d
4. Для запуска теста make test или docker compose -f docker-compose.test.yml up -d
4. API будет доступно по http://127.0.0.1:8000/docs#/
5. Результаты теста в Logs контейнера test_app.
