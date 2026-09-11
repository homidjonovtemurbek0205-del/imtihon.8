from django.contrib.auth.models import AbstractUser  # Django'ning tayyor foydalanuvchi sinfidan nusxa olish
from django.db import models  # Ma'lumotlar bazasi jadvallarini tuzish uchun ORM moduli


class User(AbstractUser):
    """
    Foydalanuvchi modeli (ER diagrammadagi 'users' jadvali)[cite: 1].
    'username' maydonida telefon raqam saqlanadi[cite: 1].
    """
    ROLE_CHOICES = (
        ("admin", "Admin"),  # Tizim administratori roli[cite: 1]
        ("user", "User"),    # Oddiy mijoz/foydalanuvchi roli[cite: 1]
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default="user"
    )  # Foydalanuvchining tizimdagi huquqini belgilovchi rol[cite: 1]

    def __str__(self):
        # Admin paneli va loglarda foydalanuvchini ko'rsatish ko'rinishi
        return f"{self.username} ({self.role})"


class Food(models.Model):
    """
    Taomlar va ichimliklar modeli (ER diagrammadagi 'Taomlar' jadvali)[cite: 1].
    """
    CATEGORY_CHOICES = (
        ("lavash", "Lavash"),
        ("ichimlik", "Ichimlik"),
        ("shirinlik", "Shirinlik"),
        ("disser", "Disser"),  # ER diagrammadagi turga mos ravishda qo'shildi[cite: 1]
        ("ovqat", "Ovqat"),
        ("snak", "Snak"),
    )
    STATUS_CHOICES = (
        ("available", "Mavjud"),
        ("unavailable", "Mavjud emas"),
    )
    
    nomi = models.CharField(max_length=255)  # Taomning nomi[cite: 1]
    narxi = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )  # Taomning narxi[cite: 1]
    turi = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES
    )  # Taomning kategoriyasi (kategoriyalar bo'yicha filterlash uchun)[cite: 1]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="available"
    )  # Taomning oshxonada bor yoki yo'qlik holati[cite: 1]

    class Meta:
        verbose_name = "Taom"
        verbose_name_plural = "Taomlar"

    def __str__(self):
        return f"{self.nomi} - {self.narxi} so'm"


class Order(models.Model):
    """
    Buyurtmalar modeli (ER diagrammadagi 'Buyurtma' jadvali)[cite: 1].
    """
    STATUS_CHOICES = (
        ("YARATILDI", "Yaratildi"),
        ("TAYYORLANMOQDA", "Tayyorlanmoqda"),
        ("YETKAZILMOQDA", "Yetkazilmoqda"),
        ("YETKAZILDI", "Yetkazildi"),
    )  # Topshiriq matnidagi qat'iy belgilangan statuslar[cite: 1]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )  # Buyurtma bergan foydalanuvchi bilan bog'lanish (1-to-N)[cite: 1]
    jami_summa = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.0
    )  # Buyurtmaning umumiy hisoblangan summasi[cite: 1]
    manzil = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )  # Yetkazib berish manzili matn shaklida[cite: 1]
    description = models.TextField(
        null=True, 
        blank=True
    )  # Buyurtma uchun qo'shimcha izohlar[cite: 1]
    tel = models.CharField(
        max_length=20, 
        null=True, 
        blank=True
    )  # TUZATILDI: ER diagrammadagi 'tel' (bog'lanish telefon raqami) maydoni qo'shildi[cite: 1]
    lat = models.FloatField(
        null=True, 
        blank=True
    )  # Xaritadagi kenglik koordinatasi[cite: 1]
    long = models.FloatField(
        null=True, 
        blank=True
    )  # Xaritadagi uzunlik koordinatasi[cite: 1]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="YARATILDI"
    )  # Buyurtmaning hozirgi holati[cite: 1]
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Buyurtma yaratilgan vaqt (avtomatik biriktiriladi)[cite: 1]
    delivered_at = models.DateTimeField(
        null=True, 
        blank=True
    )  # Buyurtma yetkazib berilgan vaqt[cite: 1]

    class Meta:
        ordering = ["-created_at"]  # Eng yangi buyurtmalarni birinchi ko'rsatish
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.user.username} ({self.status})"


class OrderItem(models.Model):
    """
    Buyurtma tarkibidagi har bir taom va uning miqdori (ER diagrammadagi 'BuyurtmaItem' jadvali)[cite: 1].
    """
    buyurtma = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items"
    )  # Tegishli buyurtma obyekti bilan bog'lanish (1-to-N)[cite: 1]
    ovqat = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE
    )  # Tanlangan taom bilan bog'lanish[cite: 1]
    soni = models.PositiveIntegerField(
        default=1
    )  # Buyurtma qilingan taomlar soni/miqdori[cite: 1]
    narxi = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )  # Buyurtma berilgan vaqtdagi taomning asl narxi[cite: 1]

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        return f"{self.soni} x {self.ovqat.nomi} (Buyurtma #{self.buyurtma.id})"