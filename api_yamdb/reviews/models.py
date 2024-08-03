from django.db import models


class Category(models.Model):
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    rating = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'


# class Review(models.Model):
#     title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
#     text = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField()
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

#     def __str__(self):
#         return self.text[:20]

#     class Meta:
#         verbose_name = 'отзыв'
#         verbose_name_plural = 'Отзывы'


# class Comment(models.Model):
#     title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
#     review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
#     text = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

#     def __str__(self):
#         return self.text[:20]

#     class Meta:
#         verbose_name = 'комментарий'
#         verbose_name_plural = 'Комментарии'
