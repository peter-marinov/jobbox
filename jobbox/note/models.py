from PIL.ImageCms import DESCRIPTION
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class UserNote(models.Model):
    TITLE_MAX_LEN = 30
    DESCRIPTION_MAX_LEN = 300

    date = models.DateTimeField(
        auto_now_add=True,
    )

    title = models.CharField(
        max_length=TITLE_MAX_LEN,
    )

    description = models.TextField(
        max_length=DESCRIPTION_MAX_LEN
    )

    user_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

