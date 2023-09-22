from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/restaurant/", include("restaurant.urls",
                                    namespace="restaurant")),
    path("api/vote/", include("vote.urls",
                              namespace="vote"))
]
