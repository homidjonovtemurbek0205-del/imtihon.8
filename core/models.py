from django.contrib.auth.models import (
    AbstractUser,
)  # Django tayyor foydalanuvchi sinfi
from django.db import models  # Modellar yaratish uchun ORM moduli


# Foydalanuvchi modeli (ER diagrammadagi users jadvali)[cite: 1]
class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),  # Admin roli
        ("user", "User"),  # Oddiy foydalanuvchi roli
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="user"
    )  # Foydalanuvchi roli[cite: 1]


# Taomlar modeli[cite: 1]
class Food(models.Model):
    CATEGORY_CHOICES = (
        ("lavash", "Lavash"),
        ("ichimlik", "Ichimlik"),
        ("shirinlik", "Shirinlik"),
        ("ovqat", "Ovqat"),
        ("snak", "Snak"),
    )
    STATUS_CHOICES = (
        ("available", "Mavjud"),
        ("unavailable", "Mavjud emas"),
    )
    nomi = models.CharField(max_length=255)  # Taom nomi[cite: 1]
    narxi = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Taom narxi[cite: 1]
    turi = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES
    )  # Taom turi[cite: 1]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )  # Holati

    def __str__(self):
        return self.nomi  # Admin panelda nomini ko'rsatish


# Buyurtma modeli[cite: 1]
class Order(models.Model):
    STATUS_CHOICES = (
        ("YARATILDI", "Yaratildi"),
        ("TAYYORLANMOQDA", "Tayyorlanmoqda"),
        ("YETKAZILMOQDA", "Yetkazilmoqda"),
        ("YETKAZILDI", "Yetkazildi"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )  # Buyurtma egasi[cite: 1]
    jami_summa = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.0
    )  # Umumiy summa[cite: 1]
    manzil = models.CharField(
        max_length=255, null=True, blank=True
    )  # Yetkazish manzili[cite: 1]
    description = models.TextField(
        null=True, blank=True
    )  # Qo'shimcha izoh[cite: 1]
    lat = models.FloatField(
        null=True, blank=True
    )  # Kenglik geolokatsiyasi[cite: 1]
    long = models.FloatField(
        null=True, blank=True
    )  # Uzunlik geolokatsiyasi[cite: 1]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="YARATILDI"
    )  # Buyurtma holati[cite: 1]
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Yaratilgan vaqti[cite: 1]
    delivered_at = models.DateTimeField(
        null=True, blank=True
    )  # Yetkazilgan vaqti[cite: 1]


# Buyurtma ichidagi taomlar modeli[cite: 1]
class OrderItem(models.Model):
    buyurtma = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )  # Tegishli buyurtma[cite: 1]
    ovqat = models.ForeignKey(
        Food, on_delete=models.CASCADE
    )  # Tanlangan taom[cite: 1]
    soni = models.PositiveIntegerField(default=1)  # Nechta buyurtma qilingani[cite: 1]
    narxi = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Biriktirilgan vaqtdagi narxi[cite: 1]