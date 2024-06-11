from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.utils.timezone import now

from .models import Task, User
from .serializers import (
    TaskSerializer, 
    CustomerTaskCreateSerializer, 
    EmployeeTaskCreateSerializer, 
    UserCreateSerializer, 
    UserReadSerializer,
)
from .permissions import (
    TaskPermission, 
    UserPermission, 
    AllTasksPermission, 
    AllEmployeesPermission,
)
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='customer').exists():
            return Task.objects.filter(customer=user.id)
        elif user.groups.filter(name='employee').exists():
            return Task.objects.filter(Q(status='pending') | Q(employee=user))
        return Task.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            user = self.request.user
            if user.groups.filter(name='customer').exists():
                return CustomerTaskCreateSerializer
            elif user.groups.filter(name='employee').exists():
                return EmployeeTaskCreateSerializer
        return TaskSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.status == 'pending':
            instance.status = 'in_progress'
            instance.employee = request.user
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        elif instance.status == 'in_progress' and instance.employee == request.user:
            instance.status = 'done'
            instance.time_closed = now()

            if request.data.get('report'):
                instance.report = request.data.get('report')
            else:
                return Response({"error": "Отчет не должен быть пустым"}, status=status.HTTP_400_BAD_REQUEST)
            
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        elif instance.status == 'done':
            return Response({"error": "Задача закрыта"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Задача уже взята другим пользователем"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        else:
            return UserReadSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password) 
        user.save()


class AllTaskView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllTasksPermission]


class AllEmployeesView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.filter(groups__name='employee')
    serializer_class = UserReadSerializer
    permission_classes = [AllEmployeesPermission]


class CurrentUserView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(pk=user.id)
