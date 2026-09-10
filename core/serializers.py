from rest_framework import serializers  # REST Framework serializer moduli

from .models import Food, Order, OrderItem, User  # Modellar importi


# Ro'yxatdan o'tish serializatori
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User  # User modeliga bog'lash
        fields = ("id", "username", "password", "role")  # Kerakli maydonlar
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Parol javobda qaytmasligi uchun

    def create(self, validated_data):
        # Parolni majburiy ravishda xeshlab yangi foydalanuvchi yaratish
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            role=validated_data.get("role", "user"),
        )


# Taomlar serializatori
class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food  # Food modeliga bog'lash
        fields = "__all__"  # Barcha maydonlarni o'z ichiga olish


# Buyurtma obyektlari serializatori
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem  # OrderItem modeliga bog'lash
        fields = ("id", "ovqat", "soni", "narxi")
        read_only_fields = ("narxi",)  # Narx taomdan olinishi uchun faqat o'qishga


# To'liq buyurtma serializatori
class OrderSerializer(serializers.ModelSerializer):
    items = (
        OrderItemSerializer(many=True)
    )  # Bitta buyurtmada bir nechta taom bo'lishi

    class Meta:
        model = Order  # Order modeliga bog'lash
        fields = (
            "id",
            "user",
            "jami_summa",
            "manzil",
            "description",
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
        )  # Tizim avtomatik hisoblaydigan maydonlar

    def create(self, validated_data):
        items_data = validated_data.pop("items")  # Items ma'lumotlarini ajratib olish
        order = Order.objects.create(**validated_data)  # Buyurtma obyektini yaratish
        total_sum = 0  # Boshlang'ich summa

        # Har bir taomni aylanib chiqish va umumiy summani hisoblash
        for item_data in items_data:
            food = item_data["ovqat"]  # Taom obyekti
            quantity = item_data["soni"]  # Nechtaligi
            total_sum += food.narxi * quantity  # Summani oshirib borish
            OrderItem.objects.create(
                buyurtma=order, ovqat=food, soni=quantity, narxi=food.narxi
            )  # Item yaratish

        order.jami_summa = total_sum  # Hisoblangan summani yozish
        order.save()  # Saqlash
        return order