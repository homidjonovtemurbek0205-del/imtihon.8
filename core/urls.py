from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import FoodViewSet, OrderViewSet, RegisterView

router = DefaultRouter()

router.register(
    r"foods", FoodViewSet, basename="food"
)

router.register(
    r"orders", OrderViewSet, basename="order"
)

urlpatterns = [
    path(
        "schema/", SpectacularAPIView.as_view(), name="schema"
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "register/", RegisterView.as_view(), name="register"
    ),
    path(
        "login/", TokenObtainPairView.as_view(), name="login"
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("", include(router.urls)),
]