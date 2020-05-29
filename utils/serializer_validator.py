from rest_framework import exceptions
from utils.exceptions import ValidationError


def validate_serializer(serializer):
    errors = []
    try:
        serializer.is_valid(raise_exception=True)
    except exceptions.ValidationError as e:
        for key, list_error in e.detail.items():
            for error in list_error:
                errors.append(f" {key}: {error.encode('utf-8').decode().lower()}")

    if errors:
        raise ValidationError(''.join(errors))
