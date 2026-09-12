import logging
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .models import Food, Order, User
from .permissions import IsAdminOrReadOnly
from .serializers import (
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)

logger = logging.getLogger("core")


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer: UserRegisterSerializer):
        user = serializer.save()
        logger.info(
            f"Yangi foydalanuvchi ro'yxatdan o'tdi: {user.username} (Role: {getattr(user, 'role', 'user')})"
        )


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all().order_by("id")
    serializer_class = FoodSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["turi", "status"]

    def perform_create(self, serializer: FoodSerializer):
        food = serializer.save()
        logger.info(
            f"Yangi taom qo'shildi: {food.nomi}, Narxi: {food.narxi}, Turi: {food.turi}"
        )

    def perform_update(self, serializer: FoodSerializer):
        old_price = self.get_object().narxi
        food = serializer.save()
        if old_price != food.narxi:
            logger.info(
                f"Taom narxi o'zgardi: {food.nomi} - Eski: {old_price}, Yangi: {food.narxi}"
            )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        user = self.request.user
        if getattr(user, "role", None) == "admin" or user.is_staff:
            return Order.objects.all().order_by("-created_at")
            
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer: OrderSerializer):
        order = serializer.save(user=self.request.user)
        logger.info(
            f"Yangi buyurtma ID: {order.id}, User: {self.request.user.username}, Summa: {order.jami_summa}"
        )

    def perform_update(self, serializer: OrderSerializer):
        user = self.request.user
        if getattr(user, "role", None) != "admin" and not user.is_staff:
            raise PermissionDenied("Buyurtma holatini faqat Admin o'zgartirishi mumkin!")

        old_status = self.get_object().status
        order = serializer.save()
        if old_status != order.status:
            logger.info(
                f"Buyurtma statusi o'zgardi ID: {order.id} - Eski: {old_status}, Yangi: {order.status}"
            )