# Домашняя работа 7.2

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

## Группы пользователей


| Группа  | Описание                                                       |
|---------|----------------------------------------------------------------|
| manager | Группа менеджеров. Может править и просматривать курсы и уроки |
| creator | Может создавать курсы и уроки                                  |