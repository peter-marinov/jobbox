from django.core.exceptions import ValidationError

INVALID_ONLY_LETTERS_MESSAGE = 'It must contain only alphabetic characters.'
INVALID_NUMBER_MESSAGE = 'Phone number must start with 0 or +.'


def check_if_only_letters(value):
    if not value.isalpha():
        raise ValidationError(INVALID_ONLY_LETTERS_MESSAGE)


def check_if_number_starts_with_zero_or_plus(value):
    if value[0] not in ['0', '+']:
        raise ValidationError(INVALID_NUMBER_MESSAGE)
