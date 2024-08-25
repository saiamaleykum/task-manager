# Task manager
## About
**EN**
Service to manage tasks within the company

**RU**
Сервис по управлению задачами внутри компании

## Installation
`docker-compose build`

`docker-compose up -d`

`python manage.py createsuperuser`

## Features 
### Authorization and auntification
- Access token
- Refresh token
### Groups
- Сustomer / Заказчик 
- Employee / Сотрудник

| Group | Permissions |
| --- | --- |
| customer | add_task, view_task |
| employee | view_task, change_task |

### Other permissions
| Permission | EN | RU |
| - | - | - |
| all_task | view all tasks | просмотр всех задач
| all_employees | view all employees | просмотр всех сотрудников
| add_user | add a new user (employee/customer) | создание нового пользователя (сотрудник/заказчик)
| view_user | view all users (employees and customers) | просмотр всех пользователей (и сотрудников, и заказчиков)

## Stack 

- Django
- DRF
- PostgreSQL
- Docker
