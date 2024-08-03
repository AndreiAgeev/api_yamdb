from datetime import datetime
from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Category
        lookup_field = 'slug',


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'name', 'slug'
        )
        model = Genre
        lookup_field = 'slug',


class TitleFullSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='name'
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        if value > datetime.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли'
            )
        return value


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title
