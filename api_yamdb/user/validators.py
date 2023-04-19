import re

from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" зарезервировано в системе'
        )


def pattern_validator(value):
    if not re.search(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            f'Недопустимые символы "{value}"'
        )
