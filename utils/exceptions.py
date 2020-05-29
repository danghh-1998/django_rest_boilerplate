from rest_framework.exceptions import APIException


class Unauthenticated(APIException):
    status_code = 200
    default_detail = 'Unauthenticated'
    default_code = '600'

    def __init__(self, message=None):
        if message:
            self.default_detail = message
        super().__init__()


class Unauthorized(APIException):
    status_code = 200
    default_detail = 'You do not have permission to perform this action.'
    default_code = '601'


class ValidationError(APIException):
    status_code = 200
    default_detail = 'The input value is invalid'
    default_code = '602'

    def __init__(self, message=None):
        if message:
            self.default_detail = message
        super().__init__()


class InvalidToken(APIException):
    status_code = 200
    default_detail = 'Invalid token'
    default_code = '603'

    def __init__(self, message=None):
        if message:
            self.default_detail = message
        super().__init__()


class TokenExpired(APIException):
    status_code = 200
    default_detail = 'Token expired'
    default_code = '604'

    def __init__(self, message=None):
        if message:
            self.default_detail = message
        super().__init__()


class ObjectNotFound(APIException):
    status_code = 200
    default_detail = 'Not found'
    default_code = '605'


class DuplicateEntry(APIException):
    status_code = 200
    default_detail = ''
    default_code = '606'

    def __init__(self, entry, key):
        self.default_detail = f"Duplicate entry {entry} for key {key}"
        super().__init__()
