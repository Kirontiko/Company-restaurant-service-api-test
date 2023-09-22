from restaurant.models import Restaurant, Dish, DishType


def sample_restaurant(id=0):
    defaults = {
        "name": f"Sample Restaurant{id}",
    }

    return Restaurant.objects.create(**defaults)


def sample_dish(id=0, **params):
    defaults = {
        "name": f"Sample Dish{id}",
        "description": "Sample Description",
    }
    defaults.update(params)

    return Dish.objects.get_or_create(**defaults)[0]


def sample_dish_type():
    return DishType.objects.create(name="Sample Dish Type")
