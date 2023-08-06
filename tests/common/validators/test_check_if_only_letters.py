from django.test import TestCase
from django.core.exceptions import ValidationError

from jobbox.common.validators import check_if_only_letters, INVALID_ONLY_LETTERS_MESSAGE


class CheckIfOnlyLettersTests(TestCase):
    def test_validate_value__when_only_letters__expect_nothing(self):
        value = 'Testname'
        check_if_only_letters(value)

    def test_validate_value__when_not_only_letters__expect_raise(self):
        value = 'Test1'
        with self.assertRaises(ValidationError) as context:
            check_if_only_letters(value)

        self.assertIsNotNone(context.exception)
        self.assertEqual(INVALID_ONLY_LETTERS_MESSAGE, context.exception.message)
        