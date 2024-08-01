from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from api.models import Title

# Узнать, откуда импортировать новую модель
User = get_user_model


class Reviews(models.Model):
    """Модель для отзывов."""

    text = models.TextField('Текст отзыва')
    score = models.PositiveIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text


class Comments(models.Model):
    """Модель для отзывов."""

    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text


class Rating(models.Model):
    """Рейтинг. Я реализовал без модели, но решил оставить заглушку."""

    pass
