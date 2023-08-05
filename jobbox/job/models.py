from django.core import validators
from django.db import models

from jobbox.app_auth.models import AppUser
from jobbox.job.validators import FileSizeValidatorInMB, validate_pdf_file


class Job(models.Model):
    """
    Model, which describes the fields for a job.
    """
    TITLE_MAX_LEN = 30
    PROGRAMMING_LANGUAGE_MAX_LEN = 15
    SALARY_MIN_VALUE = 0
    SALARY_MAX_VALUE = 150000
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
        null=False,
        blank=False,
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
            validators.MaxValueValidator(SALARY_MAX_VALUE),
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
    PDF_FILE_MAX_SIZE_IN_MB = 2

    email = models.EmailField()

    pdf_file = models.FileField(
        upload_to='cv_pdfs',
        validators=[
            FileSizeValidatorInMB(PDF_FILE_MAX_SIZE_IN_MB),
            validate_pdf_file,
        ]
    )

    job_id = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

