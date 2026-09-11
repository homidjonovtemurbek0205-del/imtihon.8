import logging  # Tizim xatolari va hodisalarini faylga yoki konsolga yozib borish moduli
from typing import Any  # Kodda ma'lumot turlarini statik ko'rsatish (type hinting) uchun vosita

from django_filters.rest_framework import DjangoFilterBackend  # API orqali obyektlarni filterlash backend classi
from rest_framework import generics, permissions, status, viewsets  # DRF'ning tayyor ko'rinishlari, ruxsatnomalari va status kodlari
from rest_framework.exceptions import PermissionDenied  # Ruxsat yetarli bo'lmaganda 403 HTTP xatolik qaytarish uchun istisno classi
from rest_framework.pagination import PageNumberPagination  # Ma'lumotlarni sahifalarga bo'lib (pagination) qaytarish classi

from .models import Food, Order, User  # Ma'lumotlar bazasi modellari importi
from .permissions import IsAdminOrReadOnly  # Maxsus yaratilgan admin/read-only ruxsatnomasi
from .serializers import (  # JSON va model o'rtasida ma'lumotlarni o'giruvchi serializerlar
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)

# "core" nomi bilan ro'yxatdan o'tgan loggerni faollashtirish
logger = logging.getLogger("core")


class StandardResultsSetPagination(PageNumberPagination):
    """
    Topshiriq talabiga ko'ra har bir sahifada 10 ta taom/obyekt chiqaradigan pagination classi[cite: 1].
    """
    page_size = 10  # Standart holda bitta sahifaga 10 ta element ajratish[cite: 1]
    page_size_query_param = "page_size"  # Mijoz URL orqali elementlar sonini so'rashi uchun parametr kaliti (?page_size=10)
    max_page_size = 100  # Mijoz bir so'rovda eng ko'p olishi mumkin bo'lgan maksimal elementlar cheklovi


class RegisterView(generics.CreateAPIView):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazuvchi faqat POST so'rovi qabul qiluvchi API[cite: 1].
    """
    queryset = User.objects.all()  # Foydalanuvchilar ma'lumotlar to'plami
    serializer_class = UserRegisterSerializer  # Kiruvchi ma'lumotlarni validatsiya qiluvchi serializer
    permission_classes = [permissions.AllowAny]  # Hamma uchun (tizimga kirmaganlarga ham) ochiq manzil

    def perform_create(self, serializer: UserRegisterSerializer) -> None:
        """
        Obyekt bazaga saqlanayotgan vaqtda ishlaydigan ichki metod.
        """
        user = serializer.save()  # Foydalanuvchi obyektini bazaga saqlash
        
        # Ro'yxatdan o'tgan foydalanuvchi haqida log faylga xabar yozish[cite: 1]
        logger.info(
            f"Yangi foydalanuvchi ro'yxatdan o'tdi: {user.username} (Role: {getattr(user, 'role', 'user')})"
        )


class FoodViewSet(viewsets.ModelViewSet):
    """
    Taomlar ustida barcha CRUD (Create, Read, Update, Delete) amallarini bajaruvchi ViewSet.
    """
    queryset = Food.objects.all().order_by("id")  # Barcha taomlarni ID bo'yicha tartiblangan holda olish
    serializer_class = FoodSerializer  # Taomlar uchun serializer
    permission_classes = [IsAdminOrReadOnly]  # Adminlar uchun to'liq boshqaruv, oddiy userlar uchun faqat o'qish (GET)[cite: 1]
    pagination_class = StandardResultsSetPagination  # Har bir sahifada 10 tadan chiqarish uchun paginationni biriktirish[cite: 1]
    filter_backends = [DjangoFilterBackend]  # Filterlash mexanizmini ulash
    filterset_fields = ["turi", "status"]  # Taom turi va statusi bo'yicha filterlash URL parametrlarini belgilash[cite: 1]

    def perform_create(self, serializer: FoodSerializer) -> None:
        """
        Yangi taom qo'shilayotgan paytda chaqiriladigan metod[cite: 1].
        """
        food = serializer.save()  # Taomni bazaga saqlash
        
        # Yangi taom yaratilganligi haqida log yozish[cite: 1]
        logger.info(
            f"Yangi taom qo'shildi: {food.nomi}, Narxi: {food.narxi}, Turi: {food.turi}"
        )

    def perform_update(self, serializer: FoodSerializer) -> None:
        """
        Mavjud taom ma'lumotlari yangilanayotganda chaqiriladigan metod[cite: 1].
        """
        old_price = self.get_object().narxi  # Taomning yangilanishidan oldingi narxini xotirada saqlab turish
        food = serializer.save()  # Yangi ma'lumotlarni bazaga saqlash
        
        # Narx o'zgargan bo'lsa, bu haqda maxsus log yozish[cite: 1]
        if old_price != food.narxi:
            logger.info(
                f"Taom narxi o'zgardi: {food.nomi} - Eski: {old_price}, Yangi: {food.narxi}"
            )


class OrderViewSet(viewsets.ModelViewSet):
    """
    Buyurtmalarni yaratish va boshqarish ko'rinishi[cite: 1].
    """
    serializer_class = OrderSerializer  # Buyurtmalar uchun serializer
    permission_classes = [permissions.IsAuthenticated]  # Faqat avtorizatsiyadan o'tgan foydalanuvchilar kira oladi[cite: 1]

    def get_queryset(self):
        """
        Foydalanuvchi roliga mos ravishda ma'lumotlar to'plamini (QuerySet) qaytaradi[cite: 1].
        """
        # Swagger hujjati yaratilayotganda "AnonymousUser" xatoligi yuzaga kelmasligi uchun tekshiruv
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        user = self.request.user  # So'rov yuborgan foydalanuvchini olish
        
        # Agar foydalanuvchi Admin bo'lsa, barcha buyurtmalarni ko'ra oladi[cite: 1]
        if getattr(user, "role", None) == "admin" or user.is_staff:
            return Order.objects.all().order_by("-created_at")
            
        # Oddiy foydalanuvchiga faqat uning o'zi yaratgan buyurtmalar tarixi qaytadi[cite: 1]
        return Order.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer: OrderSerializer) -> None:
        """
        Yangi buyurtma yaratish va uni joriy foydalanuvchiga biriktirish[cite: 1].
        """
        order = serializer.save(user=self.request.user)  # Buyurtmaga foydalanuvchini biriktirib bazaga saqlash
        
        # Buyurtma berilganda log yozish[cite: 1]
        logger.info(
            f"Yangi buyurtma ID: {order.id}, User: {self.request.user.username}, Summa: {order.jami_summa}"
        )

    def perform_update(self, serializer: OrderSerializer) -> None:
        """
        Buyurtmani o'zgartirish (statusini yangilash) amali[cite: 1].
        """
        user = self.request.user  # So'rov yuborayotgan shaxs
        
        # XAVFSIZLIK CHEKLOVI: Admin bo'lmagan foydalanuvchiga statusni o'zgartirish taqiqlanadi (403 xatosi qaytaradi)[cite: 1]
        if getattr(user, "role", None) != "admin" and not user.is_staff:
            raise PermissionDenied("Buyurtma holatini faqat Admin o'zgartirishi mumkin!")

        old_status = self.get_object().status  # O'zgartirish kiritilishidan oldingi holat/status
        order = serializer.save()  # Yangi statusni saqlash
        
        # Status haqiqatda o'zgargan bo'lsa log yozib qo'yish[cite: 1]
        if old_status != order.status:
            logger.info(
                f"Buyurtma statusi o'zgardi ID: {order.id} - Eski: {old_status}, Yangi: {order.status}"
            )