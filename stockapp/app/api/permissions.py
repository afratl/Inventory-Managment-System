from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Login olan kullanıcılar için tam erişim (CRUD),
    Login olmayan kullanıcılar için sadece GET isteği.
    """
    def has_permission(self, request, view):
        # Eğer istek GET (SAFE_METHODS) ise herkese izin ver
        if request.method in SAFE_METHODS:
            return True
        # Diğer işlemler için kullanıcı login olmalı
        return request.user and request.user.is_authenticated