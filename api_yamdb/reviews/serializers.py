from rest_framework import serializers

from reviews.models import Comments, Reviews


class AuthorMixinForSerializer(serializers.ModelSerializer):
    """Миксин для переопределения поля автора."""

    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username')


class CommentSerializer(AuthorMixinForSerializer):
    """Сериализатор для комментариев."""

    class Meta:
        """Мета."""

        model = Comments
        fields = '__all__'


class ReviewSerializer(AuthorMixinForSerializer):
    """Сериализатор для отзывов."""

    class Meta:
        """Мета."""

        model = Reviews
        fields = '__all__'
