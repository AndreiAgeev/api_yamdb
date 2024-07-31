from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from . import serializers
from reviews.models import User


class SignUpViewSet(CreateModelMixin, GenericViewSet):
    """ViewSet, обслуживающий эндпоинт api/v1/auth/signup/."""
    queryset = User.objects.all()
    serializer_class = serializers.SignUpSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Модифицированный метод .create().

        В случае, если пользователя с заданными username и email
        не существует, то происходит его создание.
        В случае, если пользователь с заданными username и email
        существует, то сериализатор обновляет его confirmation_code
        """
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
            serializer = self.get_serializer(user, data=request.data)
        except User.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


# Эндпоинт f'{api_ver}/users/' потребует пермишен IsAdminUser
# Эндпоинт f'{api_ver}/users/me/' потребует пермишен IsAuthenticated
