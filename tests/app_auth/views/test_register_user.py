from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from importlib import import_module

from jobbox.app_auth.views import RegisterUserView


class RegisterUserViewTests(TestCase):
    VALID_USER_DATA = {
        'email': 'test@mail.bg',
        'password1': 'SomeRaNDoMPass23',
        'password2': 'SomeRaNDoMPass23',
        'first_name': 'Gosho',
        'company_name': 'Prime LTD'
    }

    INVALID_USER_DATA = {
        'email': 'test@mail.bg',
        'password1': 'SomeRaNDoM',
        'password2': 'SomeRaNDoMPass23',
        'first_name': 'Gosho',
        'company_name': 'Prime LTD'
    }

    def setUp(self):
        self.factory = RequestFactory()

    def test_crete_user__when_valid__expect_to_be_created(self):
        request = self.factory.post(reverse('register_user'), self.VALID_USER_DATA)

        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        session.save()
        request.session = session

        view = RegisterUserView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 302)  # Redirect after success

        self.assertTrue(get_user_model().objects.filter(email='test@mail.bg').exists())
        self.assertTrue(response.url, reverse('index'))  # Check the redirection URL

    def test_create_user__when_not_valid__expect_to_be_not_created(self):
        request = self.factory.post(reverse('register_user'), self.INVALID_USER_DATA)
        view = RegisterUserView.as_view()

        # Run the view
        response = view(request)

        # Assert that the form is invalid and user is not created
        self.assertEqual(response.status_code, 200)  # Form is invalid, returning to the same page
        self.assertFalse(get_user_model().objects.filter(email='test@mail.bg').exists())
