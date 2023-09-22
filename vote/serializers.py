from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from vote.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("menu", "user")

    def validate(self, attrs) -> None:
        data = super(VoteSerializer, self).validate(attrs=attrs)
        vote_date = timezone.now().date()
        Vote.validate_vote_date(vote_date, data["user"], ValidationError)
        return data


class VoteListSerializer(VoteSerializer):
    menu_title = serializers.CharField(source="menu.title", read_only=True)

    class Meta:
        model = Vote
        fields = ("id", "menu_title", "vote_date")


class VoteResultsSerializer(serializers.ModelSerializer):
    menu_id = serializers.IntegerField(source="vote.menu.id", read_only=True)
    menu_title = serializers.CharField(
        source="vote.menu.title", read_only=True
    )
    restaurant_name = serializers.CharField(
        source="restaurant.name", read_only=True
    )
    total_votes = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ("menu_id", "menu_title", "restaurant_name", "total_votes")
