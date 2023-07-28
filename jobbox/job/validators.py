from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class FileSizeValidatorInMB(BaseValidator):
    def __init__(self, limit_value_in_mb):
        super().__init__(limit_value_in_mb)
        self.limit_value_in_mb = limit_value_in_mb
        self.limit_value_in_bytes = limit_value_in_mb * 1024 * 1024
        self.message = f'File is bigger than {self.limit_value_in_mb} MB'

    def __call__(self, value):
        if value.size > self.limit_value_in_bytes:
            raise ValidationError(self.message)

