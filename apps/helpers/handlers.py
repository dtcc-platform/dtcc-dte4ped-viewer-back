from rest_framework import status
from rest_framework.views import exception_handler

from apps.helpers.responses import UnauthorizedResponse


def response_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if response is not None and response.status_code == status.HTTP_401_UNAUTHORIZED:
        return UnauthorizedResponse()
