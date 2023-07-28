from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from jobbox.common.validators import check_if_only_letters, check_if_number_starts_with_zero_or_plus
from jobbox.job.validators import FileSizeValidatorInMB

UserModel = get_user_model()


class ProfileHR(models.Model):
    FIRST_NAME_MAX_LEN = 30
    LAST_NAME_MAX_LEN = 30
    COMPANY_NAME_MAX_LEN = 15
    TELEPHONE_NUMBER_MAX_LEN = 13
    TELEPHONE_NUMBER_MIN_LEN = 4
    PROFILE_PICTURE_MAX_SIZE_IN_MB = 1

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        null=True,
        blank=False,
        validators=[
            check_if_only_letters,
        ]
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        null=True,
        blank=True,
        validators=[
            check_if_only_letters,
        ]
    )

    company_name = models.CharField(
        max_length=COMPANY_NAME_MAX_LEN,
        null=True,
        blank=True,
    )

    profile_picture = models.ImageField(
        upload_to='profilehr',
        null=True,
        blank=True,
        validators=[
            FileSizeValidatorInMB(PROFILE_PICTURE_MAX_SIZE_IN_MB)
        ]
    )

    telephone_number = models.CharField(
        max_length=TELEPHONE_NUMBER_MAX_LEN,
        null=True,
        blank=True,
        validators=[
            validators.MinLengthValidator(TELEPHONE_NUMBER_MIN_LEN),
            check_if_number_starts_with_zero_or_plus,
        ]
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def full_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}'

    class Meta:
        verbose_name_plural = 'Profile HRs'


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

    class Meta:
        ordering = ['-pk']
        verbose_name_plural = 'Contact Us'
