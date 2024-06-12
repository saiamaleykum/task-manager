### Запуск
`docker-compose build`
`docker-compose up`

`python manage.py createsuperuser`

### Группы
Заказчик (customer) 
Сотрудник (employee) 

| Группа | Права |
| --- | --- |
| customer | add_task и view_task |
| employee | view_task и change_task |

### Другие права
- all_task - просмотр всех задач
- all_employees - просмотр всех сотрудников
- add_user - создание нового пользователя (сотрудник/заказчик)
- view_user - просмотр всех пользователей (и сотрудников, и заказчиков)