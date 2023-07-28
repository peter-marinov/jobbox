from django.core import validators
from django.db import models

from jobbox.app_auth.models import AppUser
from jobbox.job.validators import FileSizeValidatorInMB


class Job(models.Model):
    """
    Model, which describes the fields for a job.
    """
    TITLE_MAX_LEN = 30
    PROGRAMMING_LANGUAGE_MAX_LEN = 15
    SALARY_MIN_VALUE = 0
    DESCRIPTION_MIN_LEN = 20
    DESCRIPTION_MAX_LEN = 300
    COMPANY_LOG_MAX_SIZE_IN_MB = 1

    title = models.CharField(
        null=False,
        blank=False,
        max_length=TITLE_MAX_LEN
    )

    company_logo = models.ImageField(
        upload_to='companies_logo',
        null=True,
        blank=True,
        validators=(
            FileSizeValidatorInMB(COMPANY_LOG_MAX_SIZE_IN_MB),
        )
    )
    
    programming_language = models.CharField(
        null=False,
        blank=False,
        max_length=PROGRAMMING_LANGUAGE_MAX_LEN
    )
    
    salary = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            validators.MinValueValidator(SALARY_MIN_VALUE),
        )
    )

    description = models.TextField(
        null=False,
        blank=False,
        validators=(
            validators.MinLengthValidator(DESCRIPTION_MIN_LEN),
            validators.MaxLengthValidator(DESCRIPTION_MAX_LEN),
        )
    )

    hr = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )


class UploadCV(models.Model):
    email = models.EmailField()

    pdf_file = models.FileField(
        upload_to='cv_pdfs'
    )

    job_id = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

