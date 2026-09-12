from django.db import transaction  
from rest_framework import serializers 

from .models import Food, Order, OrderItem, User


# Ro'yxatdan o'tish serializatori
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "role")
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data: dict):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            role=validated_data.get("role", "user"),
        )


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__" 


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem 
        fields = ("id", "ovqat", "soni", "narxi")
        read_only_fields = ("narxi",)


# To'liq buyurtma serializatori
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "jami_summa",
            "manzil",
            "description",
            "tel",
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
        ) 

    @transaction.atomic
    def create(self, validated_data: dict):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        total_sum = 0 

        for item_data in items_data:
            food = item_data["ovqat"]
            quantity = item_data["soni"]
            
            total_sum += food.narxi * quantity
            
            OrderItem.objects.create(
                buyurtma=order,
                ovqat=food,
                soni=quantity,
                narxi=food.narxi,
            )
        order.jami_summa = total_sum
        order.save()
        
        return order