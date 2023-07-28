from django.core.exceptions import ValidationError


def check_if_only_letters(value):
    if not value.isalpha():
        raise ValidationError('It must contain only alphabetic characters.')


def check_if_number_starts_with_zero_or_plus(value):
    if value[0] not in ['0', '+']:
        raise ValidationError('Phone number must start with 0 or +.')