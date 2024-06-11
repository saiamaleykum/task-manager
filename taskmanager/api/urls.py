from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskViewSet, 
    UserViewSet, 
    AllTaskView, 
    AllEmployeesView, 
    CurrentUserView,
)


router = DefaultRouter()

router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)
router.register(r'all/tasks', AllTaskView, basename='all_task')
router.register(r'all/employees', AllEmployeesView, basename='all_employees')
router.register(r'currentuser', CurrentUserView, basename='my_profile')


urlpatterns = [
    path('', include(router.urls)),
]