from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
)  # HTTP xavfsiz metodlari (GET, HEAD, OPTIONS) va asosiy BasePermission classi


class IsAdminOrReadOnly(BasePermission):
    """
    Faqat Admin foydalanuvchilar uchun to'liq boshqaruv (POST, PUT, DELETE) va 
    barcha foydalanuvchilar (hatto ro'yxatdan o'tmaganlar) uchun faqat o'qish (GET) huquqini beruvchi sinf[cite: 1].
    """

    def has_permission(self, request, view) -> bool:
        # Agar so'rov turi xavfsiz metodlar (GET, HEAD, OPTIONS) bo'lsa, kirishga ruxsat beriladi
        if request.method in SAFE_METHODS:
            return True

        # O'zgartirish kiritish so'rovlarida foydalanuvchi tizimga kirganligi va roli 'admin' ekanligi tekshiriladi[cite: 1]
        # getattr() funksiyasi AnonymousUser obyekti kelganda AttributeError xatoligi chiqishining oldini oladi
        return bool(
            request.user 
            and request.user.is_authenticated 
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )


class IsAdminUser(BasePermission):
    """
    Faqat 'admin' roliga ega bo'lgan yoki is_staff belgisi bor foydalanuvchilarga barcha harakatlar uchun ruxsat beruvchi sinf[cite: 1].
    Bu klass buyurtma statusini o'zgartirish va admin amallarini cheklash uchun ishlatiladi[cite: 1].
    """

    def has_permission(self, request, view) -> bool:
        # Foydalanuvchi avtorizatsiyadan o'tganligini va roli admin ekanligini tasdiqlash[cite: 1]
        return bool(
            request.user 
            and request.user.is_authenticated 
            and (getattr(request.user, "role", None) == "admin" or request.user.is_staff)
        )