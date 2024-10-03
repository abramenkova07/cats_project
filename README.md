#  Проект Выставка котят

## Описание проекта

Проект «Выставка котят» — это API, в рамках которого:
* администратор создает список пород
* любые пользователи могут просматривать котят и породы, а также фильтровать котят по породам
* авторизованные пользователи могут создавать своих котят и оценивать чужих котят
* авторизованные пользователи могут изменять и удалять своих котят и свои оценки

## Стек использованных технологий

Проект представляет собой **API**, состоящий из **backend** части.
* **Backend:** СУБД PostgreSQL (для контейнеризации), СУБД SQLite (для разработки), Django Rest Framework
* **Контейнеризация:** Docker, Gunicorn, nginx

## Заполнение файла .env

В файле `.env` отражается конфиденциальная информация, а также определяется DEBUG и СУБД.
Склонируйте репозитарий и создайте аналогичный файл в корневой папке проекта.
```bash
git clone https://github.com/abramenkova07/cats_project.git
```
Файл `.env` должен иметь следующий вид: <br>
```python
POSTGRES_DB=cats_project
POSTGRES_USER=cats_user
POSTGRES_PASSWORD=cats_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<секретный ключ>
DEBUG=<false или true>
ALLOWED_HOSTS=localhost 127.0.0.1
USE_SQLITE=<false или true>
```

## Локальное развертывание проекта
После клонирования проекта и создания файла `.env`(где DEBUG=true, USE_SQLITE=true) выполните следующие команды в терминале:
* Создание и активация виртуального окружения:
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```
* Переходим в корневой папке в папку `cats_project/` и устанавливаем все используемые модули:
  ```bash
  cd cats_project/
  pip install -r requirements.txt
  ```
* Выполнение миграции и запуск проекта:
  ```bash
  python manage.py migrate
  python manage.py runserver
  ```
Теперь вам доступна документация по проекту по ссылкам: <br>
* [Swagger](http://127.0.0.1:8000/swagger/)
* [Redoc](http://127.0.0.1:8000/redoc/)

## Локальная контейнеризация проекта

После клонирования проекта и создания файла `.env`(где DEBUG=false, USE_SQLITE=false) выполните следующие команды в терминале:
* Создание и активация виртуального окружения:
  ```bash
  python -m venv venv
  source venv/Scripts/activate
  ```
* Создание контейнеров:
  ```bash
  docker compose up
  ```
* Последовательно выполните следующие команды в другом терминале: <br>
  ```bash
  docker compose exec backend python manage.py migrate
  DJANGO_SUPERUSER_PASSWORD=<ваш пароль> docker compose exec backend python manage.py createsuperuser --username=<логин> --email=<email> --noinput  
  docker compose exec backend python manage.py collectstatic
  docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
  ```

#### Автор проекта:
[Арина Абраменкова](https://github.com/abramenkova07)