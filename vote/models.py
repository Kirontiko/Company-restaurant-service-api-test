from django.db import models

from restaurant.models import Menu
from user.models import User


class Vote(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="votes")
    menu = models.ForeignKey(Menu,
                             on_delete=models.CASCADE,
                             related_name="votes")
