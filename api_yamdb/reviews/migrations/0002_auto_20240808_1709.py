# Generated by Django 3.2 on 2024-08-08 14:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=2024, message='Нельзя добавлять произведения, которые еще не вышли.')], verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default=1, verbose_name='Биография'),
            preserve_default=False,
        ),
    ]
