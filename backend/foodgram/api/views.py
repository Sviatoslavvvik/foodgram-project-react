from django.contrib.auth import get_user_model
from recipes.models import Ingridient, Tag
from rest_framework import viewsets

from .serializers import IngridientSerializer, TagSerializer

User = get_user_model()


class IngridientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
