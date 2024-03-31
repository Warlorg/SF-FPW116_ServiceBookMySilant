from rest_framework import permissions


class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Менеджеры').exists()


class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.vehicle.customer.user == request.user


class IsServiceDepartment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.service_department.user == request.user


class IsAdminOrManagerOrClientOrServiceDepartment(permissions.BasePermission):
    def has_permission(self, request, view):
        is_admin_or_manager = IsAdminOrManager().has_permission(request, view)
        if is_admin_or_manager:
            return True

        is_client = IsClient().has_permission(request, view)
        if is_client:
            return True

        is_service_department = IsServiceDepartment().has_permission(request, view)
        if is_service_department:
            return True

        return False
