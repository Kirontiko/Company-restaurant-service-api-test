from django.db import models
from rest_framework.exceptions import ValidationError


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    dish_type = models.ForeignKey(
        DishType, on_delete=models.CASCADE, related_name="dishes"
    )
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Menu(models.Model):
    title = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
    day = models.DateField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish, related_name="menus")

    @staticmethod
    def validate_day(day, restaurant, error_to_raise) -> None:
        if Menu.objects.filter(day=day).filter(restaurant=restaurant).exists():
            raise error_to_raise(
                {"day": "You`ve already upload menu today! Try again tomorrow"}
            )

    def clean(self) -> None:
        Menu.validate_day(self.day, self.restaurant, ValidationError)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ) -> None:
        self.full_clean()
        return super(Menu, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return self.title
