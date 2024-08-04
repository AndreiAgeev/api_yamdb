from django.contrib import admin

from .models import Category, Comments, Genre, Reviews, Title


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Reviews)
admin.site.register(Comments)
