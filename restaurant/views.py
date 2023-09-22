from typing import Type

from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from permissions import IsAdminOrIfAuthenticatedReadOnly
from restaurant.models import (
    Restaurant,
    DishType,
    Dish,
    Menu,
)
from restaurant.serializers import (
    RestaurantSerializer,
    DishTypeSerializer,
    DishSerializer,
    DishListSerializer,
    DishDetailSerializer,
    MenuSerializer,
    MenuListSerializer,
)
from vote.models import Vote
from vote.serializers import VoteSerializer


class RestaurantViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class DishTypeViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = DishType.objects.all()
    serializer_class = DishTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class DishViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Dish.objects.select_related("dish_type")
    serializer_class = DishSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return DishListSerializer
        if self.action == "retrieve":
            return DishDetailSerializer
        return DishSerializer


class MenuViewSet(
    CreateModelMixin, ListModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = MenuSerializer
    today = timezone.now().date()
    queryset = (
        Menu.objects.filter(day=today)
        .select_related("restaurant")
        .prefetch_related("dishes")
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "list":
            return MenuListSerializer

        return MenuSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = serializer.instance

        response_data = {
            "title": instance.title,
            "restaurant": instance.restaurant.name,
            "day": instance.day,
            "dishes": [dish.name for dish in instance.dishes.all()],
        }

        headers = self.get_success_headers(serializer.data)
        return Response(
            response_data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="menu-history",
    )
    def menu_history(self, request) -> Response:
        menus = Menu.objects.select_related("restaurant").prefetch_related(
            "dishes"
        )
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=True,
        url_path="vote",
    )
    def vote(self, request, pk=None) -> Response:
        menu = self.get_object()
        user = request.user

        serializer = VoteSerializer(data={"menu": menu.id, "user": user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "message": "Your vote was successfully added!",
            "menu": menu.title,
            "restaurant": menu.restaurant.name,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
