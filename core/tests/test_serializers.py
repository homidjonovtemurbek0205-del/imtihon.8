from core.models import Food, User  # Testlar uchun zarur bo'lgan modellar importi[cite: 1]
from core.serializers import (  # Tekshirilishi kerak bo'lgan serializerlar[cite: 1]
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)
from django.test import TestCase  # Django'ning standart birlik (unit) test sinfi[cite: 1]


class SerializerTestCase(TestCase):
    """
    Serializer'larning validatsiya va ma'lumotlarni to'g'ri saqlash hamda hisoblash mantiqini tekshiruvchi test sinfi[cite: 1].
    """

    def setUp(self):
        """
        Har bir test ishga tushishidan oldin ma'lumotlar bazasida yaratiladigan boshlang'ich obyektlar[cite: 1].
        """
        # Test uchun foydalanuvchi yaratish[cite: 1]
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        # Test uchun taom obyekti yaratish (narxi: 35000)[cite: 1]
        self.food = Food.objects.create(
            nomi="Osh", narxi=35000, turi="ovqat", status="available"
        )

    def test_user_register_serializer(self):
        """
        UserRegisterSerializer orqali foydalanuvchini ro'yxatdan o'tkazish validatsiyasini va saqlanishini tekshirish[cite: 1].
        """
        data = {
            "username": "998901234567",  # Telefon raqam sifatida username[cite: 1]
            "password": "password123",
            "role": "user",
        }
        serializer = UserRegisterSerializer(data=data)
        
        # Kiruvchi ma'lumotlar validatsiyadan to'g'ri o'tganligini tekshirish[cite: 1]
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()  # Foydalanuvchini saqlash[cite: 1]
        
        # Username to'g'ri saqlanganligini tasdiqlash[cite: 1]
        self.assertEqual(user.username, "998901234567")

    def test_food_serializer(self):
        """
        FoodSerializer obyekt ma'lumotlarini JSON korinishiga to'g'ri seriatsiyalashini tekshirish[cite: 1].
        """
        serializer = FoodSerializer(instance=self.food)
        
        # Chiqish ma'lumotlaridagi 'nomi' maydoni obyekt nomi bilan bir xilligini tekshirish[cite: 1]
        self.assertEqual(serializer.data["nomi"], "Osh")

    def test_order_serializer_calculation(self):
        """
        OrderSerializer buyurtma yaratilayotganda jami summani (35000 * 2 = 70000) avtomatik to'g'ri hisoblashini tekshirish[cite: 1].
        """
        data = {
            "manzil": "Toshkent",
            "tel": "+998901234567",
            "items": [{"ovqat": self.food.id, "soni": 2}],  # 2 ta Osh buyurtma qilish[cite: 1]
        }
        serializer = OrderSerializer(data=data)
        
        # Ma'lumotlar to'g'riligini (valid) tekshirish[cite: 1]
        self.assertTrue(serializer.is_valid())
        
        # Buyurtmaga foydalanuvchini biriktirib saqlash[cite: 1]
        order = serializer.save(user=self.user)
        
        # Jami summa avtomatik 70000 bo'lganini va bazaga yozilganini tekshirish[cite: 1]
        self.assertEqual(order.jami_summa, 70000)