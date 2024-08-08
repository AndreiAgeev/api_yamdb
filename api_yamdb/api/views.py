from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from . import permisions, serializers
from .filters import TitleFilter
from .mixin import CreateListDestroyMixin
from reviews.models import Category, Genre, Review, Title, User


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
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
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
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.request.user


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (permisions.AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete', 'head')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.TitleListSerializer
        return serializers.TitleFullSerializer

    def response_data(self, data):
        """Заменяет в данных сериализатора поля genre и category,
        добавляя туда объекты их сериализаторов."""
        genres = data.pop('genre')
        genre_list = list()
        for genre in genres:
            genre_obj = Genre.objects.get(slug=genre)
            genre_list.append(serializers.GenreSerializer(genre_obj).data)
        data['genre'] = genre_list
        category = data.pop('category')
        category_obj = Category.objects.get(slug=category)
        data['category'] = serializers.CategorySerializer(category_obj).data
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = self.response_data(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            response_data, status=status.HTTP_201_CREATED, headers=headers
        )


class BaseForGenreAndCategoryViewSet(
    CreateListDestroyMixin, viewsets.GenericViewSet
):
    permission_classes = (permisions.AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(BaseForGenreAndCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class CategoryViewSet(BaseForGenreAndCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс обработки отзывов."""

    serializer_class = serializers.ReviewSerializer
    pk_url_kwarg = 'review_id'
    permission_classes = (permisions.UserStaffOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        """Забираю необходимое произведение."""
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title, author=self.request.user)
        # Пересчитываю значение рейтинга при создании отзыва
        self.rating_calculating()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Пересчитываю значение рейтинга при удалении отзыва
        self.rating_calculating()

    def partial_update(self, request, *args, **kwargs):
        # Если при изменении отзыва (patch) пришла оценка -> перерасчет
        if 'score' in request.data:
            super().partial_update(request, *args, **kwargs)
            self.rating_calculating()
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Запрет PUT-запросов
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            # Разрешение PATCH-запросов
            return super().update(request, *args, **kwargs)

    def rating_calculating(self):
        """Пересчет рейтинга произведения."""
        title = self.get_title()
        reviews = self.get_queryset()
        if reviews.count() > 0:
            title_rating = reviews.aggregate(average=Avg('score'))['average']
            title.rating = title_rating
            title.save()


class CommentViewSet(viewsets.ModelViewSet):
    """Класс обработки комментариев."""

    serializer_class = serializers.CommentSerializer
    permission_classes = (permisions.UserStaffOrReadOnly,)
    pagination_class = LimitOffsetPagination
    pk_url_kwarg = 'comment_id'
    http_method_names = ('get', 'post', 'patch', 'delete', 'head')

    def get_review(self):
        # Забираю отзыв.
        review_id = self.kwargs['review_id']
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.select_related('author')

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
