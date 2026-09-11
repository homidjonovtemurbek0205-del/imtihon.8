from django.urls import include, path  # API marshrutlarini belgilash va boshqa URL guruhlarini ulash moduli
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)  # Swagger OpenAPI v3 hujjatlarini generatsiya qiluvchi ko'rinishlar (drf-spectacular)
from rest_framework.routers import DefaultRouter  # ViewSet'lar uchun standart RESTful URL marshrutlarini yaratuvchi router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Foydalanuvchi login va parolini tekshirib, JWT tokenlar (access va refresh) beruvchi API[cite: 1]
    TokenRefreshView,  # Eskirgan access tokenni refresh token orqali yangilab beruvchi API[cite: 1]
)

from .views import FoodViewSet, OrderViewSet, RegisterView  # Barcha yaratilgan controller/view klasslari importi

# ViewSet'lar uchun avtomatik URL yaratuvchi router obyektini e'lon qilish
router = DefaultRouter()

# FoodViewSet uchun /foods/ va /foods/{id}/ marshrutlarini avtomatik ro'yxatga olish[cite: 1]
router.register(
    r"foods", FoodViewSet, basename="food"
)

# OrderViewSet uchun /orders/ va /orders/{id}/ marshrutlarini avtomatik ro'yxatga olish[cite: 1]
router.register(
    r"orders", OrderViewSet, basename="order"
)

urlpatterns = [
    # OpenAPI sxemasini JSON ko'rinishida shakllantiruvchi endpoint
    path(
        "schema/", SpectacularAPIView.as_view(), name="schema"
    ),
    
    # Swagger UI vizual interfeysi (/api/docs/ orqali barcha API'larni sinab ko'rish imkonini beradi)[cite: 1]
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    
    # Yangi foydalanuvchini ro'yxatdan o'tkazish endpointi (/api/register/)[cite: 1]
    path(
        "register/", RegisterView.as_view(), name="register"
    ),
    
    # JWT Auth: Tizimga kirish (login) va juftlik tokenlarini olish endpointi (/api/login/)[cite: 1]
    path(
        "login/", TokenObtainPairView.as_view(), name="login"
    ),
    
    # JWT Auth: Access tokenni yangilash endpointi (/api/token/refresh/)[cite: 1]
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    
    # Router tomonidan avtomatik shakllantirilgan /foods/ va /orders/ yo'nalishlarini umumiy ro'yxatga ulash
    path("", include(router.urls)),
]