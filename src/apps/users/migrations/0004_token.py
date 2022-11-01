# Generated by Django 4.1 on 2022-08-16 18:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_last_modified_alter_user_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Creation datetime of folder.", verbose_name="created at"
                    ),
                ),
                (
                    "last_modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Last modification datetime of folder.",
                        verbose_name="last modified at",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="User custom label for token for identification.",
                        max_length=50,
                        verbose_name="label",
                    ),
                ),
                ("key", models.CharField(help_text="Value of token.", max_length=255, unique=True, verbose_name="key")),
                (
                    "valid_until",
                    models.DateTimeField(help_text="Datetime when token expires.", verbose_name="valid until"),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="User's token.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tokens",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="token owner",
                    ),
                ),
            ],
            options={
                "verbose_name": "token",
                "verbose_name_plural": "tokens",
                "ordering": ("label",),
            },
        ),
    ]
