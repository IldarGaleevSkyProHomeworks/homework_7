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
