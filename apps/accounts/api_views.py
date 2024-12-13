from django.contrib.auth import authenticate
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.accounts.serializers import UserSerializer, LoginSerializer
from apps.helpers.responses import SuccessResponse, BadRequestResponse


class AccountsViewSet(viewsets.GenericViewSet):
    permission_classes_by_action = {
        "secure_endpoint": [IsAuthenticated],
        "default": [AllowAny]
    }
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, ]

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action["default"]]

    def get_serializer_context(self):
        context = super(AccountsViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        else:
            return UserSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_response_serializer_class(self):
        return UserSerializer

    def get_response_serializer(self, *args, **kwargs):
        serializer_class = self.get_response_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @action(methods=['post'], detail=False)
    def login(self, request, *arg, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = authenticate(request=request, **validated_data)
        if user:
            serializer = self.get_response_serializer(user, many=False)
            return SuccessResponse({
                "user": serializer.data,
                "token": AuthToken.objects.create(user)[1]
            })

        return BadRequestResponse(error="Wrong credentials")

    # temporary actions
    @action(methods=['get', 'post'], detail=False)
    def secure_endpoint(self, request, *args, **kwargs):
        return SuccessResponse({})

    @action(methods=['get', 'post'], detail=False)
    def unsecure_endpoint(self, request, *args, **kwargs):
        return SuccessResponse({})
