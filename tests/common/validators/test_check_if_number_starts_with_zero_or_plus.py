from django.test import TestCase
from django.core.exceptions import ValidationError

from jobbox.common.validators import check_if_number_starts_with_zero_or_plus, INVALID_NUMBER_MESSAGE


class ValidatePhoneTests(TestCase):
    def test_validate_phone__when_starts_with_zero__expect_nothing(self):
        phone_number = '0123456'
        check_if_number_starts_with_zero_or_plus(phone_number)

    def test_validate_phone__when_starts_with_plus__expect_nothing(self):
        phone_number = '+123456'
        check_if_number_starts_with_zero_or_plus(phone_number)

    def test_validate_phone__when_not_starts_with_zero_or_plus__expect_raise(self):
        phone_number = '4123456'
        with self.assertRaises(ValidationError) as context:
            check_if_number_starts_with_zero_or_plus(phone_number)

        self.assertIsNotNone(context.exception)
        self.assertEqual(INVALID_NUMBER_MESSAGE, context.exception.message)