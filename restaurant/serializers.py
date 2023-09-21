from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from restaurant.models import (
    Restaurant,
    DishType,
    Dish,
    Menu,
)


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name"
        )


class DishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishType
        fields = (
            "id",
            "name"
        )


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "dish_type",
            "description",
        )


class DishListSerializer(DishSerializer):
    dish_type_name = serializers.CharField(
        source="dish_type.name",
        read_only=True
    )

    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "dish_type_name",
            "description"
        )


class DishDetailSerializer(DishSerializer):
    dish_type_name = serializers.CharField(
        source="dish_type.name",
        read_only=True,
    )

    class Meta:
        model = Dish
        fields = (
            "id",
            "name",
            "dish_type_name",
            "description",
        )


class MenuSerializer(serializers.ModelSerializer):
    def validate(self, attrs) -> None:
        data = super(MenuSerializer, self).validate(attrs=attrs)
        day = timezone.now().date()
        Menu.validate_day(day, ValidationError)
        return data

    class Meta:
        model = Menu
        fields = (
            "id",
            "title",
            "restaurant",
            "day",
            "dishes"
        )


class MenuListSerializer(MenuSerializer):
    restaurant_name = serializers.CharField(
        source="restaurant.name",
        read_only=True
    )
    dishes = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )

    class Meta:
        model = Menu
        fields = (
            "id",
            "title",
            "restaurant_name",
            "day",
            "dishes"
        )
