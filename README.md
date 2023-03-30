# Статистика рекламы.

Небольшой сервис на основе FastAPI, Postgresql и sqlmodel для работы со статистикой.

## Запуск проекта

1. Скорпируйте код проекта
2. Запустите проект в docker compose введя следующую команду

```sh
$ docker-compose up -d --build
```

## Доступные эндпоинты

Swagger документация доступка по ссылке [http://0.0.0.0:8004/docs](http://0.0.0.0:8004/docs)

### Получение статистики

Получить статистику [http://localhost:8004/stats](http://localhost:8004/stats)
Параметры строки могут быть следующими:

- from_date - обязательное поле, дата в формате YYYY-MM-DD
- to_date - обязательное поле, дата в формате YYYY-MM-DD
- sort - в поле нужно передать поле для сортировки по нему: "views", "clicks", "cost", "cpc", "cpm", "id" ("date" по умолчанию).
- sort_by_desc - True/False при передаче sort для того чтобы сортировка была обратной.

Простой запрос с датами

```sh
$ curl -X 'GET' \
  'http://0.0.0.0:8004/stats?from_date=2023-01-30&to_date=2023-03-01' \
  -H 'accept: application/json'
```

Запрос с датами, и полем "cpm" для обратной сортировки.

```sh
$ curl -X 'GET' \
  'http://0.0.0.0:8004/stats?from_date=2023-01-30&to_date=2023-03-01&sort=cpm&sort_by_desc=true' \
  -H 'accept: application/json'
```

### Сохранение статистики

```sh
$ curl -X 'POST' \
  'http://0.0.0.0:8004/stats?date=2023-02-23&views=12343&clicks=754&cost=2.5' \
  -H 'accept: application/json' \
  -d ''
```

### Сбросить статистику

```sh
$ curl -X 'DELETE' \
  'http://0.0.0.0:8004/stats' \
  -H 'accept: application/json'
```
