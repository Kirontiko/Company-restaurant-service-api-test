from rest_framework import routers

from restaurant.views import (
    RestaurantViewSet,
    DishTypeViewSet,
    DishViewSet,
    MenuViewSet,
)

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("dish_types", DishTypeViewSet)
router.register("dishes", DishViewSet)
router.register("menus", MenuViewSet, basename="menu")


urlpatterns = router.urls

app_name = "restaurant"
