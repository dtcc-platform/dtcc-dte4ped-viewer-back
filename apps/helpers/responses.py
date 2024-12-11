from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class SuccessResponse(Response):
    def __init__(self, data=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        super(SuccessResponse, self).__init__(None, status=status.HTTP_200_OK)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        success_data = {"success": True, "data": data}
        self.data = success_data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


class BadRequestResponse(Response):
    def __init__(self, error=None, errors=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        super(BadRequestResponse, self).__init__(None, status=status.HTTP_400_BAD_REQUEST)

        if isinstance(error, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)
        if error:
            failure_data = {"success": False, "error": error}
        else:
            failure_data = {"success": False, "errors": errors}

        self.data = failure_data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


class UnauthorizedResponse(Response):
    def __init__(self, error=None, errors=None, data=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        super(UnauthorizedResponse, self).__init__(None, status=status.HTTP_401_UNAUTHORIZED)

        if isinstance(error, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        if errors:
            failure_data = {"success": False, "errors": errors}
        else:
            failure_data = {
                "success": False,
                "error": error or "Authentication credentials were not provided or are invalid."
            }

        self.data = failure_data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


