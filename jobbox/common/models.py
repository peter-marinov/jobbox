from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from jobbox.app_auth.models import AppUser

# Create your models here.
UserModel = get_user_model()


class Profile(models.Model):
    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class ProfileHR(models.Model):
    first_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    company_name = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class ContactUs(models.Model):
    TOPIC_MAX_LEN = 20
    DESCRIPTION_MIN_LEN = 20
    DESCRIPTION_MAX_LEN = 300

    email = models.EmailField()

    topic = models.CharField(
        max_length=TOPIC_MAX_LEN,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LEN,
        validators=(
            validators.MinLengthValidator(DESCRIPTION_MIN_LEN),
        )
    )