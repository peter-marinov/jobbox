from django.test import TestCase

from jobbox.task.forms import HRTaskForm
from jobbox.task.models import HRTask


class HRTaskFormTests(TestCase):
    def test_hr_task__when_form_valid_data__expect_valid_form(self):
        form_data = {
            'task': 'Test HR Task',
            'status': HRTask.NOT_STARTED,
        }
        form = HRTaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_hr_task__when_form_missing_data__expect_form_not_valid(self):
        form_data = {
            'task': '',
            'status': '',
        }
        form = HRTaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_hr_task__when_task_too_long__expect_not_valid_form(self):
        long_task = 'a' * (HRTask.TASK_MAX_LEN + 1)
        form_data = {
            'task': long_task,
            'status': HRTask.NOT_STARTED,
        }
        form = HRTaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('task' in form.errors)

    def test_hr_task__when_invalid_status__expect_not_valid_form(self):
        form_data = {
            'task': 'Test HR Task',
            'status': 'Invalid Status',
        }
        form = HRTaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('status' in form.errors)
        