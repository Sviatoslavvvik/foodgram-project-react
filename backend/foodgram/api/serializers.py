from django.contrib.auth import get_user_model
from recipes.models import Ingridient, Tag
from rest_framework import serializers

User = get_user_model()


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag
