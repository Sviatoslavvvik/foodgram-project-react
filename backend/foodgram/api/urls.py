from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngridientViewSet, TagViewSet

api_router = DefaultRouter()
api_router.register('ingredients',
                    IngridientViewSet, basename='ingredients')
api_router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(api_router.urls)),
]
