from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleFullSerializer,
    TitleListSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title
from .mixin import CreateListDestroyMixin
from .import serializers
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


class GetTokenView(TokenObtainPairView):
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
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TitleListSerializer
        return TitleFullSerializer


class BaseForGenreAndCategoryViewSet(
    CreateListDestroyMixin, viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(BaseForGenreAndCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(BaseForGenreAndCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
