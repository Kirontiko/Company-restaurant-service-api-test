from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer
from restaurant.tests.model_samples import sample_restaurant

RESTAURANT_URL = reverse("restaurant:restaurant-list")


class UnauthenticatedRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_authenticate_required(self):
        response = self.client.get(RESTAURANT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRestaurantTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "testuser", "testpass123"
        )
        self.client.force_authenticate(self.user)

    def test_list_restaurants(self):
        for i in range(5):
            sample_restaurant(i)
        response = self.client.get(RESTAURANT_URL)

        expected_restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(expected_restaurants, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_restaurant(self):
        restaurant = sample_restaurant()

        url = reverse(
            "restaurant:restaurant-detail", args=[restaurant.id]
        )
        res = self.client.get(url)

        serializer = RestaurantSerializer(restaurant)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_restaurant_create_forbidden(self):
        payload = {"name": "Sample Restaurant"}
        res = self.client.post(RESTAURANT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminRestaurantApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_restaurant(self):
        payload = {"name": "Sample Restaurant"}
        res = self.client.post(RESTAURANT_URL, payload)
        restaurant = Restaurant.objects.get(id=res.data["id"])

        restaurants = Restaurant.objects.all()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(restaurant, restaurants)

    def test_delete_restaurant(self):
        restaurant = sample_restaurant()

        url = reverse(
            "restaurant:restaurant-detail", args=[restaurant.id]
        )
        restaurant = Restaurant.objects.get(id=restaurant.id)
        res = self.client.delete(url)

        restaurants = Restaurant.objects.all()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(restaurant, restaurants)




