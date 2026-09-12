from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default="user"
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class Food(models.Model):
    CATEGORY_CHOICES = (
        ("lavash", "Lavash"),
        ("ichimlik", "Ichimlik"),
        ("shirinlik", "Shirinlik"),
        ("disser", "Disser"),
        ("ovqat", "Ovqat"),
        ("snak", "Snak"),
    )
    STATUS_CHOICES = (
        ("available", "Mavjud"),
        ("unavailable", "Mavjud emas"),
    )
    
    nomi = models.CharField(max_length=255)
    narxi = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    turi = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="available"
    )

    class Meta:
        verbose_name = "Taom"
        verbose_name_plural = "Taomlar"

    def __str__(self):
        return f"{self.nomi} - {self.narxi} so'm"


class Order(models.Model):
    STATUS_CHOICES = (
        ("YARATILDI", "Yaratildi"),
        ("TAYYORLANMOQDA", "Tayyorlanmoqda"),
        ("YETKAZILMOQDA", "Yetkazilmoqda"),
        ("YETKAZILDI", "Yetkazildi"),
    )

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )
    jami_summa = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.0
    )
    manzil = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    description = models.TextField(
        null=True, 
        blank=True
    )
    tel = models.CharField(
        max_length=20, 
        null=True, 
        blank=True
    )
    lat = models.FloatField(
        null=True, 
        blank=True
    )
    long = models.FloatField(
        null=True, 
        blank=True
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="YARATILDI"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    delivered_at = models.DateTimeField(
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    buyurtma = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items"
    )
    ovqat = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE
    )
    soni = models.PositiveIntegerField(
        default=1
    )
    narxi = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        return f"{self.soni} x {self.ovqat.nomi} (Buyurtma #{self.buyurtma.id})"