from django.core.exceptions import ValidationError
import re


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя "me" зарезервировано в системе'
        )


# def slug_validator(value):
#     if not re.search(r'^[-a-zA-Z0-9_]+$', value):
#         raise ValidationError(
#             f'Недопустимые символы "{value}" в slug'
#         )
