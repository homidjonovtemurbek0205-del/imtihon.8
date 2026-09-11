from core.models import Food, Order, User  # Testlarda ishlatiladigan modellar importi[cite: 1]
from django.urls import reverse  # API yo'llarining nomlari bo'yicha URL manzillarini aniqlovchi funktsiya
from rest_framework import status  # HTTP javob statuse kodlari to'plami
from rest_framework.test import APITestCase  # Django REST Framework uchun maxsus API test klassi


class APITestCaseViews(APITestCase):
    """
    API endpointlarini test qiluvchi asosiy test klassi[cite: 1].
    """

    def setUp(self):
        """
        Har bir test bajarilishidan oldin avtomatik ravishda tayyorlanadigan boshlang'ich ma'lumotlar[cite: 1].
        """
        # Admin rolidagi foydalanuvchini bazada yaratish[cite: 1]
        self.admin = User.objects.create_user(
            username="admin_user", password="password123", role="admin"
        )
        # Oddiy 'user' rolidagi foydalanuvchini bazada yaratish[cite: 1]
        self.user = User.objects.create_user(
            username="simple_user", password="password123", role="user"
        )
        # Boshlang'ich taom obyektini yaratish[cite: 1]
        self.food = Food.objects.create(
            nomi="Lavash", narxi=30000, turi="lavash", status="available"
        )

    def test_get_foods(self):
        """
        Taomlar ro'yxatini olish (GET /api/foods/) barcha uchun ochiq ekanligini tekshirish[cite: 1].
        """
        response = self.client.get(reverse("food-list"))  # GET so'rovini yuborish
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Javob kodi 200 OK bo'lishini tekshirish

    def test_admin_create_food(self):
        """
        Admin vakolatiga ega foydalanuvchi yangi taom qo'sha olishini tekshirish (POST)[cite: 1].
        """
        self.client.force_authenticate(
            user=self.admin
        )  # Tizimga admin sifatida avtorizatsiyadan o'tib kirish
        data = {
            "nomi": "Cola",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")  # POST so'rovini yuborish
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )  # Javob kodi 201 Created bo'lishini tekshirish

    def test_user_cannot_create_food(self):
        """
        Oddiy foydalanuvchi yangi taom qo'sha olmasligini tekshirish (xavfsizlik testi)[cite: 1].
        """
        self.client.force_authenticate(
            user=self.user
        )  # Tizimga oddiy foydalanuvchi sifatida kirish
        data = {
            "nomi": "Fanta",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Admin bo'lmagani uchun 403 Forbidden qaytishini tekshirish[cite: 1]

    def test_create_order_authenticated_user(self):
        """
        Tizimga kirgan foydalanuvchi muvaffaqiyatli buyurtma bera olishini tekshirish[cite: 1].
        """
        self.client.force_authenticate(user=self.user)  # Oddiy user sifatida kirish
        data = {
            "manzil": "Toshkent sh., Yunusobod tumani",
            "tel": "+998901234567",
            "items": [
                {"ovqat": self.food.id, "soni": 2}  # 2 ta Lavash buyurtma qilish[cite: 1]
            ]
        }
        response = self.client.post(reverse("order-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )  # Buyurtma yaratilganligini (201 Created) tasdiqlash
        self.assertEqual(
            Order.objects.count(), 1
        )  # Bazada 1 ta buyurtma saqlanganligini tekshirish

    def test_user_cannot_change_order_status(self):
        """
        Oddiy foydalanuvchi buyurtma statusini o'zgartira olmasligini tekshirish[cite: 1].
        """
        # Boshlang'ich buyurtma yaratib olish
        order = Order.objects.create(user=self.user, jami_summa=30000, status="YARATILDI")
        
        self.client.force_authenticate(user=self.user)  # Oddiy user sifatida kirish
        data = {"status": "YETKAZILDI"}  # Statusni o'zgartirishga urinish
        
        # Detail URL orqali PATCH so'rovi yuborish
        response = self.client.patch(
            reverse("order-detail", kwargs={"pk": order.id}), data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Admin bo'lmagani uchun taqiqlanishi kerak[cite: 1]