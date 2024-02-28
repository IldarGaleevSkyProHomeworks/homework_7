from rest_framework import permissions


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
        return obj.owner == request.user if hasattr(obj, 'owner') else False


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_manager


class IsContentCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_creator
