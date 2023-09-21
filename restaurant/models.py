from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    dish_type = models.ForeignKey(DishType,
                                  on_delete=models.CASCADE,
                                  related_name="dishes")
    description = models.TextField(null=True, blank=True)


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Menu(models.Model):
    title = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE,
                                   related_name="menus")
    day = models.DateField(auto_now_add=True)
    dishes = models.ManyToManyField(Dish, related_name="menus")
