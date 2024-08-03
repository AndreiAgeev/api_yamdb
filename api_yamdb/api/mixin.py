from rest_framework import viewsets, mixins


class CreateListDestroyMixin(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    "Кастомный миксин класс"
    pass
