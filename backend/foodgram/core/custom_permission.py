from rest_framework import permissions


class AuthorChangePermission(permissions.BasePermission):
    """Разрешение на изменение только автором"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class UserDeletePermission(permissions.BasePermission):
    """Разрешение на удаление только пользователем"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if view.action == 'favorite':
            return obj.favorite_receip.filter(user=request.user).exists()
        return obj.shopping_chart_receip.filter(user=request.user).exists()
