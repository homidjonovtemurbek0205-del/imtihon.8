from core.models import Food, Order, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APITestCaseViews(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_user", password="password123", role="admin"
        )
        self.user = User.objects.create_user(
            username="simple_user", password="password123", role="user"
        )
        self.food = Food.objects.create(
            nomi="Lavash", narxi=30000, turi="lavash", status="available"
        )

    def test_get_foods(self):
        response = self.client.get(reverse("food-list"))
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_admin_create_food(self):
        self.client.force_authenticate(
            user=self.admin
        )
        data = {
            "nomi": "Cola",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )

    def test_user_cannot_create_food(self):
        self.client.force_authenticate(
            user=self.user
        )
        data = {
            "nomi": "Fanta",
            "narxi": 10000,
            "turi": "ichimlik",
            "status": "available",
        }
        response = self.client.post(reverse("food-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_create_order_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "manzil": "Toshkent sh., Yunusobod tumani",
            "tel": "+998901234567",
            "items": [
                {"ovqat": self.food.id, "soni": 2}
            ]
        }
        response = self.client.post(reverse("order-list"), data, format="json")
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Order.objects.count(), 1
        )

    def test_user_cannot_change_order_status(self):
        order = Order.objects.create(user=self.user, jami_summa=30000, status="YARATILDI")
        
        self.client.force_authenticate(user=self.user)
        data = {"status": "YETKAZILDI"}
        
        response = self.client.patch(
            reverse("order-detail", kwargs={"pk": order.id}), data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )