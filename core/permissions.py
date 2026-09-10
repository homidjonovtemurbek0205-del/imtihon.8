from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)  # Xavfsiz metodlar va asosiy permisssion sinfi


# Admin va o'qish uchun maxsus ruxsatnoma
class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Agar so'rov GET, HEAD, OPTIONS bo'lsa hamma ko'ra oladi
        if request.method in SAFE_METHODS:
            return True
        # Aks holda foydalanuvchi tizimga kirgan va 'admin' roliga ega bo'lishi shart
        return (
            request.user.is_authenticated and request.user.role == "admin"
        )