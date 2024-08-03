from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleFullSerializer,
    TitleListSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title
from .mixin import CreateListDestroyMixin


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
