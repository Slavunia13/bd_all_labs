# Лабораторные по предмету Базы Данных, 2024г.

## Описание

Данных проект является реализацией всех лабораторных работ по предмету Базы Данных

Все нужные бд поднимаются в виде отдельных docker контейнеров, все данные для подключения указываются в .env

Для подключения используются разные классы в /app/db/connection, работа классов описана в комментариях

Чтобы не париться с фронтенд фреимворками, весь интерфейс описан через простенькие html файлы в /pages

Для обработки и перенаправления запросов используется nginx

Посмотреть api можно по localhost:8080/swagger


В 3 лабе агрегационный поиск фактически отсутствует, если кто допишет кидайте мне на почту, буду рад)

## Запуск сервиса

### Требования:

- Docker
- Docker-compose

### Запуск:

1. Создать `.env` файл и добавить в него необходимые параметры окружения `make env`

2. Можно сбилдить все без запуска `make build`

3. Запуск (собирает образы, если их нет) `make run`

## Подключение

- Граф. интерфейс: http://localhost
- OpenApi: http://localhost:8080/openapi
- Swagger: http://localhost:8080/swagger


Выполнил Кирпиченко Вячеслав, группа 22305
