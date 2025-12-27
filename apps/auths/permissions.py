from rest_framework.permissions import BasePermission


class IsUnauthenticatedUser(BasePermission):
    """Allow access only when the request user is not authenticated."""

    message = "This endpoint is only available to unauthenticated users."

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        user = getattr(request, "user", None)
        return not user or not user.is_authenticated
