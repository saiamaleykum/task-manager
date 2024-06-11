from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Сотрудник'),
        ('customer', 'Заказчик'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)

    class Meta:
        permissions = [
            ("all_employees", "Can view all employees"),
        ]


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает исполнителя'),
        ('in_progress', 'В процессе'),
        ('done', 'Выполнена'),
    ]

    customer = models.ForeignKey(
        User, 
        verbose_name='created_by', 
        on_delete=models.CASCADE, 
        related_name="created_tasks",
    )
    employee = models.ForeignKey(
        User, verbose_name='taken_by', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="taken_tasks",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_closed= models.DateTimeField(null=True, blank=True)
    report = models.TextField(null=True, blank=True)

    class Meta:
        permissions = [
            ("all_task", "Can view all tasks"),
        ]