from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Title
from reviews.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Reviews


class ReviewViewSet(viewsets.ModelViewSet):
    """Класс обработки отзывов."""

    serializer_class = ReviewSerializer
    pk_url_kwarg = 'review_id'
    permission_classes = (IsAuthenticatedOrReadOnly,)
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
        # Если при изменении отзыва пришла оценка, делаю перерасчет
        if 'score' in request.data:
            super().partial_update(request, *args, **kwargs)
            self.rating_calculating()
        return super().partial_update(request, *args, **kwargs)

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

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_review(self):
        """Забираю отзыв."""
        review_id = self.kwargs['review_id']
        return get_object_or_404(Reviews, pk=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        review = self.get_review()
        return get_object_or_404(review.comments, pk=comment_id)
