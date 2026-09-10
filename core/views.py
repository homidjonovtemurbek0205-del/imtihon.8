import logging  # Tizim hodisalarini (log) yozib borish uchun Python standart kutubxonasi

from django_filters.rest_framework import (
    DjangoFilterBackend,
)  # API so'rovlarida filterlashni ta'minlovchi backend vositasi
from rest_framework import (
    generics,
    permissions,
    viewsets,
)  # DRF tayyor ko'rinishlari (views) va ruxsatnomalar to'plami

from .models import Food, Order, User  # Baza modellari importi
from .permissions import IsAdminOrReadOnly  # Maxsus tayyorlangan ruxsatnoma
from .serializers import (  # Ma'lumotlarni JSON shakliga o'tkazuvchi serializerlar
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)

logger = logging.getLogger("core")  # "core" nomi bilan log yozuvchi obyektni faollashtirish


# Foydalanuvchilarni ro'yxatdan o'tkazish ko'rinishi
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  # Foydalanuvchilar ma'lumotlar bazasi to'plami
    serializer_class = UserRegisterSerializer  # Ishlatiladigan serializer sinfi
    permission_classes = [permissions.AllowAny]  # Har qanday foydalanuvchi (tizimga kirmagan ham) kirishi mumkin

    def perform_create(self, serializer):
        # Obyekt ma'lumotlar bazasiga saqlanayotgan paytdagi amallar
        user = serializer.save()  # Foydalanuvchini bazaga saqlash
        logger.info(
            f"Yangi foydalanuvchi ro'yxatdan o'tdi: {user.username} (Role: {user.role})"
        )  # Tizim jurnaliga muvaffaqiyatli ro'yxatdan o'tganlik haqida yozish


# Taomlar bilan bog'liq CRUD amallari
class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all().order_by('id')  # Barcha taomlarni ID bo'yicha tartiblangan holda olish
    serializer_class = FoodSerializer  # Taomlar uchun serializer
    permission_classes = [IsAdminOrReadOnly]  # Faqat admin o'zgartira oladi, qolganlar faqat ko'ra oladi
    filter_backends = [DjangoFilterBackend]  # Filterlash mexanizmini ulash
    filterset_fields = ["turi", "status"]  # URL orqali 'turi' va 'status' bo'yicha filter qilish imkoni

    def perform_create(self, serializer):
        # Yangi taom qo'shilayotgan paytda
        food = serializer.save()  # Taomni bazaga saqlash
        logger.info(
            f"Yangi taom qo'shildi: {food.nomi}, Narxi: {food.narxi}, Turi: {food.turi}"
        )  # Logga yangi taom haqida xabar yozish

    def perform_update(self, serializer):
        # Mavjud taom ma'lumotlari o'zgartirilayotgan paytda
        old_price = self.get_object().narxi  # Taomning saqlashdan oldingi eski narxini eslab qolish
        food = serializer.save()  # Yangilangan ma'lumotlarni saqlash
        if old_price != food.narxi:  # Agar narx o'zgargan bo'lsa
            logger.info(
                f"Taom narxi o'zgardi: {food.nomi} - Eski: {old_price}, Yangi: {food.narxi}"
            )  # Narx o'zgargani haqida log yozish


# Buyurtmalarni boshqarish ko'rinishi
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer  # Buyurtmalar uchun serializer
    permission_classes = [permissions.IsAuthenticated]  # Faqat authorization (login) qilgan foydalanuvchilar kirishi mumkin

    def get_queryset(self):
        # Swagger schema generatsiyasi paytida AnonymousUser xatolik bermasligi uchun tekshiruv
        if getattr(self, "swagger_fake_view", False):
            return Order.objects.none()

        # Foydalanuvchi roliga qarab ma'lumot qaytarish mantiqi
        if self.request.user.role == "admin":  # Agar so'rov yuborgan shaxs admin bo'lsa
            return Order.objects.all().order_by("-created_at")  # Barcha buyurtmalarni eng yangisidan boshlab qaytarish
        return Order.objects.filter(user=self.request.user).order_by("-created_at")  # Oddiy foydalanuvchiga faqat o'zining buyurtmalarini qaytarish

    def perform_create(self, serializer):
        # Buyurtma yaratilayotganda
        order = serializer.save(user=self.request.user)  # Buyurtmachi sifatida joriy foydalanuvchini biriktirish va saqlash
        logger.info(
            f"Yangi buyurtma ID: {order.id}, User: {self.request.user.username}, Summa: {order.jami_summa}"
        )  # Logga buyurtma va uning summasini yozish

    def perform_update(self, serializer):
        # Buyurtma holati/statusi o'zgartirilayotganda
        old_status = self.get_object().status  # O'zgartirishdan oldingi eski statusni olish
        order = serializer.save()  # Yangilanishni saqlash
        if old_status != order.status:  # Status haqiqatdan ham o'zgargan bo'lsa
            logger.info(
                f"Buyurtma statusi o'zgardi ID: {order.id} - Eski: {old_status}, Yangi: {order.status}"
            )  # Status o'zgargani haqida logga yozib qo'yish