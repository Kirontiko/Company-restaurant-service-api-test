from rest_framework import routers

from vote.views import VoteViewSet


router = routers.DefaultRouter()
router.register("votes", VoteViewSet)


urlpatterns = router.urls

app_name = "vote"