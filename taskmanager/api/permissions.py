from rest_framework import permissions


class TaskPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user and request.user.has_perm('api.add_task')
        elif view.action in ['list', 'retrieve']:
            return request.user and request.user.has_perm('api.view_task')
        elif view.action == 'partial_update':
            return request.user and request.user.has_perm('api.change_task')
        elif view.action in ['update', 'destroy']:
            return False
        return True


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user and request.user.has_perm('api.add_user')
        elif view.action in ['list', 'retrieve']:
            return request.user and request.user.has_perm('api.view_user')
        return True


class AllTasksPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user and request.user.has_perm('api.all_task')
        

class AllEmployeesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user and request.user.has_perm('api.all_employees')
