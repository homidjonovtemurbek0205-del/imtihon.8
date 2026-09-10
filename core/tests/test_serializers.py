from core.models import Food, User  # Modellar importi
from core.serializers import (  # Serializerlar importi
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)
from django.test import TestCase  # Django test moduli


class SerializerTestCase(TestCase):

    def setUp(self):
        # Boshlang'ich test ma'lumotlarini yaratish
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.food = Food.objects.create(
            nomi="Osh", narxi=35000, turi="ovqat", status="available"
        )

    def test_user_register_serializer(self):
        # Ro'yxatdan o'tish serializatori to'g'riligini tekshirish
        data = {
            "username": "998901234567",
            "password": "password123",
            "role": "user",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(
            serializer.is_valid()
        )  # Ma'lumot to'g'ri (valid) ekanligini tasdiqlash
        user = serializer.save()  # Saqlash
        self.assertEqual(
            user.username, "998901234567"
        )  # Ism to'g'ri saqlanganini tekshirish

    def test_food_serializer(self):
        # Taom serializatori to'g'ri chiqish ma'lumotini shakllantirishini tekshirish
        serializer = FoodSerializer(instance=self.food)
        self.assertEqual(
            serializer.data["nomi"], "Osh"
        )  # Nom mos kelishini tekshirish

    def test_order_serializer_calculation(self):
        # Buyurtmada jami summa avtomatik to'g'ri hisoblanishini tekshirish
        data = {
            "manzil": "Toshkent",
            "items": [{"ovqat": self.food.id, "soni": 2}],
        }
        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save(user=self.user)
        self.assertEqual(
            order.jami_summa, 70000
        )  # 35000 * 2 = 70000 ekanligini tasdiqlash