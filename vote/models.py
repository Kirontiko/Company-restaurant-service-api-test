from django.db import models
from rest_framework.exceptions import ValidationError

from restaurant.models import Menu
from user.models import User


class Vote(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="votes")
    menu = models.ForeignKey(Menu,
                             on_delete=models.CASCADE,
                             related_name="votes")
    vote_date = models.DateField(auto_now_add=True)

    @staticmethod
    def validate_vote_date(vote_date, user, error_to_raise) -> None:
        if Vote.objects.filter(vote_date=vote_date).filter(user=user).exists():
            raise error_to_raise(
                {
                    "day":
                        "You`ve already voted today! Try again tomorrow"
                }
            )

    def clean(self) -> None:
        Vote.validate_vote_date(self.vote_date, self.user, ValidationError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ) -> None:
        self.full_clean()
        return super(Vote, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    def __str__(self):
        return f"{self.menu.title} - {self.vote_date}"
