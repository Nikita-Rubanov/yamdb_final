import datetime as dt

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
        )


def validate_year(year: int) -> None:
    if dt.datetime.now().year < year:
        raise ValidationError("year not valid value")
