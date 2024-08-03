from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


api_ver = 'v1'

router = DefaultRouter()
# router.register('auth/signup', views.SignUpViewSet)
router.register('titles', views.TitleViewSet)
router.register('genres', views.GanreViewSet)
router.register('categories', views.CategoryViewSet)


urlpatterns = [
    path(f'{api_ver}/', include(router.urls))
]