# nodoc - don't add to the documentation wiki

from .base_exception import BaseException


class ValidationError(BaseException):
    pass
