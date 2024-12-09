from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class SuccessResponse(Response):
    def __init__(self, data=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
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

