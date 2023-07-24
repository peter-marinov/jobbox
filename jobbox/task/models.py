from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class HRTask(models.Model):
    TASK_MAX_LEN = 50
    STATUS_MAX_LEN = 20

    NOT_STARTED = 'Not started'
    WORKING = 'Working'
    ON_HOLD = 'On hold'
    DONE = 'Done'

    hr_task_choices = (
        (NOT_STARTED, NOT_STARTED),
        (WORKING, WORKING),
        (ON_HOLD, ON_HOLD),
        (DONE, DONE)
    )

    date = models.DateTimeField(
        auto_now_add=True,
    )

    task = models.CharField(
        max_length=TASK_MAX_LEN,
    )

    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        choices=hr_task_choices,
        default=NOT_STARTED
    )

    user_id = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['pk']
