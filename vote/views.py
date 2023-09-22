from django.db.models import Count, QuerySet
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from restaurant.models import Menu
from vote.models import Vote
from vote.serializers import VoteResultsSerializer, VoteListSerializer


class VoteViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return Vote.objects.filter(user=self.request.user).select_related(
            "menu"
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="vote-results",
    )
    def vote_results(self, request) -> Response:
        today = timezone.now().date()
        menus_with_votes = (
            Menu.objects.filter(day=today)
            .annotate(total_votes=Count("votes"))
        )
        sorted_menus = menus_with_votes.order_by("-total_votes")

        serializer = VoteResultsSerializer(sorted_menus, many=True)

        return Response(serializer.data)
