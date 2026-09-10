from django.urls import include, path  # Yo'naltirish modullari
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)  # Swagger hujjatlarini hosil qiluvchi ko'rinishlar
from rest_framework.routers import DefaultRouter  # ViewSet uchun avto-router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Login qilish (JWT Token olish)
    TokenRefreshView,  # Access tokenni yangilash
)

from .views import FoodViewSet, OrderViewSet, RegisterView

router = DefaultRouter()  # Avto-router obyekti
router.register(
    r"foods", FoodViewSet, basename="food"
)  # /foods/ va /foods/{id}/ yo'nalishlarini avtomatik biriktirish
router.register(
    r"orders", OrderViewSet, basename="order"
)  # /orders/ va /orders/{id}/ yo'nalishlarini avtomatik biriktirish

urlpatterns = [
    # Swagger API hujjatlari
    path(
        "schema/", SpectacularAPIView.as_view(), name="schema"
    ),  # OpenAPI sxemasi (JSON fayli)
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),  # Swagger interfeysi (/api/docs/)
    # Autentifikatsiya va Ro'yxatdan o'tish
    path(
        "register/", RegisterView.as_view(), name="register"
    ),  # Foydalanuvchini ro'yxatdan o'tkazish
    path(
        "login/", TokenObtainPairView.as_view(), name="login"
    ),  # Login qilish (access va refresh token olish)
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Refresh token orqali yangi access token olish
    # Router orqali kelayotgan ViewSet yo'nalishlari
    path("", include(router.urls)),  # /foods/ va /orders/ marshrutlarini ulash
]