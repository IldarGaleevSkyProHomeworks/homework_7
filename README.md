# Домашняя работа 7.6

<div align="center">
<a href="https://wakatime.com/@IldarGaleev/projects/nijmfwmhds"><img src="https://wakatime.com/badge/user/45799db8-b1f8-4627-9264-2c8d4c352567/project/018da7e5-d70d-4460-b4eb-be7768a9c8e5.svg" alt="wakatime"></a>
<img src="https://img.shields.io/github/last-commit/IldarGaleevSkyProHomeworks/homework_7.svg"/>
</div>

## Endpoints

| path                          | methods                | filtering fields                      | ordering fields |
|-------------------------------|------------------------|---------------------------------------|-----------------|
| `/learn/courses/`             | `GET`                  |                                       |                 |
| `/learn/courses/<id>/`        | `GET`, `PUT`, `DELETE` |                                       |                 |
| `/learn/lessons/`             | `GET`                  |                                       |                 |
| `/learn/lessons/<id>`         | `GET`                  |                                       |                 |
| `/learn/lessons/<id>/change/` | `PUT`                  |                                       |                 |
| `/learn/lessons/<id>/delete/` | `DELETE`               |                                       |                 |
| `/accounts/users/`            | `GET`                  |                                       |                 |
| `/accounts/users/<id>/`       | `GET`, `PUT`, `DELETE` |                                       |                 |
| `/accounts/payments/`         | `GET`, `PUT`, `DELETE` | `payment_method`, `purchased_product` | `payment_date`  |
| `/courses/<id>/subscribe/`    | `PUSH`,`DELETE`        |                                       |                 |

## Авторизация и регистрация

| path                       | method | data                                               | описание                        |
|----------------------------|--------|----------------------------------------------------|---------------------------------|
| `/accounts/users/`         | `POST` | `{"email":"user@example.com","password":"secret"}` | регистрация нового пользователя |
| `/accounts/token/`         | `POST` | `{"email":"user@example.com","password":"secret"}` | получение токена авторизации    |
| `/accounts/token/refresh/` | `POST` | `{"refresh":"<refresh_secret>"}`                   | обновление токена авториации    |

## Группы пользователей

| Группа  | Описание                                                       |
|---------|----------------------------------------------------------------|
| manager | Группа менеджеров. Может править и просматривать курсы и уроки |
| creator | Может создавать курсы и уроки                                  |

## Перменные среды

> [!TIP]
>
> Поддерживается файл `.env` для назначения переменных. [Шаблон файла](.env.template)

### Общие

| Переменная                    | Назначение                                                                     |
|-------------------------------|--------------------------------------------------------------------------------|
| `SECRET_KEY`                  | Ключ безопасности Django                                                       |
| `DEBUG`                       | Режим отладки                                                                  |
| `DISABLE_PASSWORD_VALIDATION` | Отключить валидацию паролей пользователей (применимо только если `DEBUG=True`) |
| `LANGUAGE_CODE`               | [Код языка](http://www.i18nguy.com/unicode/language-identifiers.html)          |
| `TIME_ZONE`                   | [Часовой пояс](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)   |
| `ALLOWED_HOSTS`               | Разрешенные хосты                                                              |

### База данных

| Переменная    | Назначение                                                                                                              |
|---------------|-------------------------------------------------------------------------------------------------------------------------|
| `DB_ENGINE`   | Движок базы данных (`django.db.backends.postgresql_psycopg2` - **postgres**; `django.db.backends.sqlite3` - **sqlite**) |
| `DB_NAME`     | Имя базы данных                                                                                                         |
| `DB_USER`     | Имя пользователя для подключения                                                                                        |
| `DB_PASSWORD` | Пароль пользователя для подключения                                                                                     |
| `DB_HOST`     | Имя хоста с сервером                                                                                                    |
| `DB_PORT`     | Порт сервера                                                                                                            |

### Stripe

1. Создайте [webhook в Stripe](https://dashboard.stripe.com/test/webhooks)
2. Активируйте событие `checkout.session.completed`
3. Полученный `Signing secret` в веб-хуке пропишите в переменную `STRIPE_ENDPOINT_SECRET`
4. Добавьте адрес внешнего сетевого интерфейса (или адрес выданный вам прокси-сервером) в переменную `ALLOWED_HOSTS`

| Переменная               | Назначение                    |
|--------------------------|-------------------------------|
| `STRIPE_API_KEY`         | Ключ для доступа к API Stripe |
| `STRIPE_ENDPOINT_SECRET` | Токен для доступа к веб-хуку  |

## Celery

| Переменная                                  | Назначение                                                                   |
|---------------------------------------------|------------------------------------------------------------------------------|
| `INACTIVE_USERS_INTERVAL`                   | Интервал (дни) по истечении которого пользователь будет считаться неактивным |
| `CELERY_BROKER_URL`,`CELERY_RESULT_BACKEND` | Брокеры для Celery                                                           |
| `CELERY_TASK_RETRY_COUNT`                   | Число повторных попыток для неуспешных задач                                 |

### Команды Django

> [!TIP]
> Использование
>
> ```Bash
> python manage.py <команда>
> ```

| Команда        | Назначение                               |
|----------------|------------------------------------------|
| `creategroups` | Создает необходимые группы пользователей |


## Docker

Мнимимальная настройка для успешного развертывания контейнеров:
1. Создайте файл `.env.docker` с указанными переменными:
   - `STRIPE_API_KEY` и `STRIPE_ENDPOINT_SECRET` - [см. Stripe](#stripe)
   - `APPLICATION_HOSTNAME` - внешний адрес приложения. Используется для задания `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
   - `APPLICATION_SCHEME` (не обязательно) - по умолчанию `https`, при локальном запуске обычно не требуется.
2. В сервисе `web`
   - Создайте учетную запись администратора стандартной командой Django: `python manage.py createsuperuser`