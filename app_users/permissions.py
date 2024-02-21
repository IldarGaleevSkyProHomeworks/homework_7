from rest_framework import permissions

from app_users.apps import AppUsersConfig


class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated:
            return True
        elif not request.user.is_authenticated and request.method != "POST":
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user if hasattr(obj, 'owner') else False


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.groups.filter(name=AppUsersConfig.manager_group_name).exists()


class IsContentCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.groups.filter(name=AppUsersConfig.content_creator_group_name).exists()
