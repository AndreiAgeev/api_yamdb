from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from . import pagination, permisions, serializers
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
        существует, то сериализатор обновляет его confirmation_code.
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


class GetTokenView(TokenObtainPairView):
    """ViewSet для получения токенов."""
    serializer_class = serializers.GetTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            {'token': serializer.validated_data['token']},
            status=status.HTTP_200_OK
        )


class AdminViewSet(ModelViewSet):
    """ViewSet для функционала админов."""
    queryset = User.objects.all()
    serializer_class = serializers.AdminUsersSerializer
    permission_classes = (permisions.AdminOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = pagination.UsersListPagination
    http_method_names = ('get', 'post', 'patch', 'delete', 'head')
    lookup_field = 'username'

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_unusable_password()
        user.save()


class UserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    """ViewSet для просмотра пользователем своих данных."""
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch')

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user
