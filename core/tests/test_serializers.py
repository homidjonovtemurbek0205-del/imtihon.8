from core.models import Food, User
from core.serializers import (
    FoodSerializer,
    OrderSerializer,
    UserRegisterSerializer,
)
from django.test import TestCase


class SerializerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.food = Food.objects.create(
            nomi="Osh", narxi=35000, turi="ovqat", status="available"
        )

    def test_user_register_serializer(self):
        data = {
            "username": "998901234567",
            "password": "password123",
            "role": "user",
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "998901234567")

    def test_food_serializer(self):
        serializer = FoodSerializer(instance=self.food)

        self.assertEqual(serializer.data["nomi"], "Osh")

    def test_order_serializer_calculation(self):
        data = {
            "manzil": "Toshkent",
            "tel": "+998901234567",
            "items": [{"ovqat": self.food.id, "soni": 2}],
        }
        serializer = OrderSerializer(data=data)        
        self.assertTrue(serializer.is_valid())        
        order = serializer.save(user=self.user)
        self.assertEqual(order.jami_summa, 70000)