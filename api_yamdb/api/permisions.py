from rest_framework import permissions

STAFF_ROLES = ('moderator', 'admin')


class UserStaffOrReadOnly(permissions.BasePermission):
    """Даёт следующие доступы:
    1) для анонимов только возможность просмотра контента;
    2) для пользователей - просмотр и создание контента;
    3) для модераторов и админов - всё выше + редактирование контента
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role in STAFF_ROLES
            or request.user.is_superuser
        )


class AdminOnly(permissions.BasePermission):
    """Даёт доступ только для админов"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )
