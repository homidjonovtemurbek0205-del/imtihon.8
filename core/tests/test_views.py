from core.models import Food, User  # Modellar
from django.urls import reverse  # URL nomidan yo'lni topish
from rest_framework import status  # HTTP status kodlar
from rest_framework.test import APITestCase  # API test qilish uchun maxsus sinf


class APITestCaseViews(APITestCase):

    def setUp(self):
        # Admin, oddiy foydalanuvchi va taom obyekti yaratish
        self.admin = User.objects.create_user(
            username="admin", password="password123", role="admin"
        )
        self.user = User.objects.create_user(
            username="user", password="password123", role="user"
        )
        self.food = Food.objects.create(
            nomi="Lavash", narxi=30000, turi="lavash", status="available"
        )

    def test_get_foods(self):
        # Taomlar ro'yxatini olish API'sini tekshirish (GET)
        response = self.client.get(reverse("food-list"))
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Status 200 OK bo'lishi shart

    def test_admin_create_food(self):
        # Admin taom yarata olishini tekshirish (POST)
        self.client.force_authenticate(
            user=self.admin
        )  # Admin sifatida tizimga kirish
        data = {
            "nomi": "Cola",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )  # Status 201 Created bo'lishi shart

    def test_user_cannot_create_food(self):
        # Oddiy foydalanuvchi taom qo'sha olmasligini tekshirish
        self.client.force_authenticate(
            user=self.user
        )  # User sifatida tizimga kirish
        data = {
            "nomi": "Fanta",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )  # Status 403 Forbidden qaytishi shart