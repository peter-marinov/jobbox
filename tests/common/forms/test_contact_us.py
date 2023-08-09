from django.test import TestCase

from jobbox.common.forms import ContactUsFrom
from jobbox.common.models import ContactUs


class ContactUsFormTests(TestCase):
    VALID_DATA = {
        'email': 'test@mail.com',
        'topic': 'Test Topic',
        'description': 'Test Description put here',
    }

    def test_form__when_valid_data__expect_form_is_valid(self):
        form = ContactUsFrom(data=self.VALID_DATA)
        self.assertTrue(form.is_valid())

    def test_form__when_missing_email__expect_form_not_valid(self):
        form = ContactUsFrom(data={
            'topic': self.VALID_DATA['topic'],
            'description': self.VALID_DATA['description'],
        })

        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)

    def test_form__when_invalid_email__expect_form_not_valid(self):
        form = ContactUsFrom(data={
            'email': 'invalid-email',
            'topic': self.VALID_DATA['topic'],
            'description': self.VALID_DATA['description'],
        })

        self.assertFalse(form.is_valid())

    def test_form__when_topic_too_long__expect_form_not_valid(self):
        form = ContactUsFrom(data={
            'email': self.VALID_DATA['email'],
            'topic': 'a' * (ContactUs.TOPIC_MAX_LEN + 1),
            'description': self.VALID_DATA['description'],
        })

        self.assertFalse(form.is_valid())

    def test_form__when_description_too_short__expect_form_not_valid(self):
        form = ContactUsFrom(data={
            'email': self.VALID_DATA['email'],
            'topic': self.VALID_DATA['topic'],
            'description': 'a' * (ContactUs.DESCRIPTION_MIN_LEN - 1),
        })

        self.assertFalse(form.is_valid())

    def test_form__when_description_too_long__expect_form_not_valid(self):
        form = ContactUsFrom(data={
            'email': self.VALID_DATA['email'],
            'topic': self.VALID_DATA['topic'],
            'description': 'a' * (ContactUs.DESCRIPTION_MAX_LEN + 1),
        })

        self.assertFalse(form.is_valid())