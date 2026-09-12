from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user 
            and request.user.is_authenticated 
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )


class IsAdminUser(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user 
            and request.user.is_authenticated 
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )