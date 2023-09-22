# Generated by Django 4.2.5 on 2023-09-22 00:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("vote", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vote",
            name="vote_date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
