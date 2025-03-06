from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import BooleanField, CharField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = models.CharField(null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Phone number")
    is_active = BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("can_block_user", "can block user"),
            ("can_disabling_mailings", "can disabling mailings"),
        ]

    def __str__(self):
        return self.email
