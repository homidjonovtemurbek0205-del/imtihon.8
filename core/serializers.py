from django.db import transaction  # Baza amallarini bir butun (atomik) tranzaksiya ichida bajarish uchun
from rest_framework import serializers  # REST Framework serializer moduli

from .models import Food, Order, OrderItem, User  # Modellar importi


# Ro'yxatdan o'tish serializatori
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish va parolni xeshlab saqlash classi[cite: 1].
    """

    class Meta:
        model = User  # User modeliga bog'lash[cite: 1]
        fields = ("id", "username", "password", "role")  # Kerakli maydonlar ro'yxati[cite: 1]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Parol maxfiy saqlanishi va javob (response)da qaytmasligi uchun[cite: 1]

    def create(self, validated_data: dict) -> User:
        """
        Parolni majburiy ravishda xeshlab (create_user orqali) yangi foydalanuvchi yaratish.
        """
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            role=validated_data.get("role", "user"),  # Agar rol berilmasa, standart "user" belgilanadi[cite: 1]
        )


# Taomlar serializatori
class FoodSerializer(serializers.ModelSerializer):
    """
    Taomlar haqidagi ma'lumotlarni o'giruvchi serializer[cite: 1].
    """

    class Meta:
        model = Food  # Food modeliga bog'lash[cite: 1]
        fields = "__all__"  # Barcha maydonlarni (id, nomi, narxi, turi) o'z ichiga olish[cite: 1]


# Buyurtma tarkibidagi har bir taom serializatori
class OrderItemSerializer(serializers.ModelSerializer):
    """
    Buyurtma ichidagi taomlar ro'yxati va ularning miqdorini boshqarish[cite: 1].
    """

    class Meta:
        model = OrderItem  # OrderItem modeliga bog'lash[cite: 1]
        fields = ("id", "ovqat", "soni", "narxi")  # DB sxemasidagi maydonlar[cite: 1]
        read_only_fields = ("narxi",)  # Narx foydalanuvchi tomonidan kiritilmaydi, taom narxidan olinadi[cite: 1]


# To'liq buyurtma serializatori
class OrderSerializer(serializers.ModelSerializer):
    """
    Buyurtma berish, umumiy summani avtomatik hisoblash va tarixni ko'rish classi[cite: 1].
    """
    # Nested serializer: Bitta buyurtma tarkibida bir nechta taom bo'lishini ta'minlaydi[cite: 1]
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order  # Order modeliga bog'lash[cite: 1]
        fields = (
            "id",
            "user",
            "jami_summa",
            "manzil",
            "description",
            "tel",  # TUZATILDI: DB sxemasidagi 'tel' maydoni qo'shildi[cite: 1]
            "lat",
            "long",
            "status",
            "created_at",
            "delivered_at",
            "items",
        )
        read_only_fields = (
            "user",
            "jami_summa",
            "created_at",
        )  # Tizim tomonidan avtomatik to'ldiriladigan readonly maydonlar[cite: 1]

    @transaction.atomic
    def create(self, validated_data: dict) -> Order:
        """
        Buyurtma va unga tegishli taomlarni bir vaqtning o'zida bazaga saqlash hamda summani hisoblash.
        @transaction.atomic xatolik yuz berganda bazaga chala ma'lumot tushib qolishining oldini oladi.
        """
        # Validatsiyadan o'tgan ma'lumotlar ichidan 'items' ro'yxatini ajratib olish
        items_data = validated_data.pop("items")
        
        # Boshlang'ich buyurtma obyektini yaratish
        order = Order.objects.create(**validated_data)
        total_sum = 0  # Boshlang'ich umumiy summa

        # Har bir taomni aylanib chiqib, OrderItem yaratish va summani hisoblash
        for item_data in items_data:
            food = item_data["ovqat"]  # Tanlangan taom obyekti
            quantity = item_data["soni"]  # Taom soni/miqdori
            
            total_sum += food.narxi * quantity  # Umumiy summani oshirib borish
            
            OrderItem.objects.create(
                buyurtma=order,
                ovqat=food,
                soni=quantity,
                narxi=food.narxi,  # Hozirgi narxni saqlab qo'yish
            )

        # Hisoblangan jami summani buyurtmaga yozish va saqlash
        order.jami_summa = total_sum
        order.save()
        
        return order