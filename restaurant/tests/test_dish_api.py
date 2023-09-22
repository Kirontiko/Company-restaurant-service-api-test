from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from restaurant.models import DishType, Dish
from restaurant.serializers import DishListSerializer, DishDetailSerializer
from restaurant.tests.model_samples import sample_dish, sample_dish_type

DISH_URL = reverse("restaurant:dish-list")


class UnauthenticatedRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_authenticate_required(self):
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRestaurantTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_list_dishes(self):
        dish_type = sample_dish_type()
        for i in range(5):
            sample_dish(i, dish_type=dish_type)
        response = self.client.get(DISH_URL)

        expected_dishes = Dish.objects.all()
        serializer = DishListSerializer(expected_dishes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_dish(self):
        dish_type = sample_dish_type()
        dish = sample_dish(dish_type=dish_type)

        url = reverse(
            "restaurant:dish-detail", args=[dish.id]
        )
        res = self.client.get(url)

        serializer = DishDetailSerializer(dish)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_dish_create_forbidden(self):
        payload = {"name": "Sample Dish",
                   "dish_type": sample_dish_type().id}
        res = self.client.post(DISH_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminDishApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_dish(self):
        payload = {"name": "Sample Dish",
                   "dish_type": sample_dish_type().id}
        res = self.client.post(DISH_URL, payload)
        dish = Dish.objects.get(id=res.data["id"])

        dishes = Dish.objects.all()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(dish, dishes)

    def test_delete_restaurant(self):
        dish_type = sample_dish_type()
        dish = sample_dish(dish_type=dish_type)

        url = reverse(
            "restaurant:dish-detail", args=[dish.id]
        )
        dish = Dish.objects.get(id=dish.id)
        res = self.client.delete(url)

        dishes = Dish.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(dish, dishes)