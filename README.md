# Api_yamdb

https://github.com/Nikita-Rubanov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg

Ссылка на проект:

http://51.250.7.220/redoc/

## Описание

Проект позволяет оставлять отзывы о произведениях (фильмах, книгах, музыке и т.д.).
самих произведений он не содержит.

## Запуск проекта

Клонируем репозиторий к себе на ПК

```bash
  git clone git@github.com:Nikita-Rubanov/infra_sp2.git
```

Создайте файл .env в директории /infra для работы с базой данных.
Заполните его по шаблону:

```bash
  DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
  DB_NAME=postgres # имя базы данных
  POSTGRES_USER=postgres # логин для подключения к базе данных
  POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
  DB_HOST=db # название сервиса (контейнера)
  DB_PORT=5432 # порт для подключения к БД
```


Поднимаем контейнеры

```bash
  docker-compose up -d --build
```

выполнгяем миграции:

```bash
  docker-compose exec web python manage.py makemigrations reviews

  docker-compose exec web python manage.py migrate
```

Создаем суперпользователя

```bash
  docker-compose exec web python manage.py createsuperuser
```

Србираем статику

```bash
  docker-compose exec web python manage.py collectstatic --no-input
```

Наполняем бд данными из файла fixtures.json
```bash
  docker-compose exec web python manage.py loaddata fixtures.json
```

