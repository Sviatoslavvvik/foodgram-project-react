from django.contrib.auth import get_user_model
from recipes.models import IngredientInRecipe, Ingridient, Receipe, Tag
from rest_framework import serializers
from users.serializers import UserProfileSerializer

from .models import Favorite

User = get_user_model()


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingridient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngridientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингридиентов в рецепте"""
    id = serializers.PrimaryKeyRelatedField(source='ingridient',
                                            read_only=True)
    name = serializers.SlugRelatedField(source='ingridient',
                                        slug_field='name',
                                        read_only=True)
    measurment_unit = serializers.SlugRelatedField(
        source='ingridient',
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id',
            'name',
            'measurment_unit',
            'amount'
        )


class ReceipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserProfileSerializer(read_only=True)
    ingredients = IngridientInRecipeSerializer(
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Receipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_user_from_request(self):
        request = self.context.get('request')
        return request, request.user

    def get_is_favorited(self, obj):
        request, user = self.get_user_from_request()
        if request is None or user.is_anonymous:
            return False
        return user.favorites.filter(receipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request, user = self.get_user_from_request()
        if request is None or user.is_anonymous:
            return False
        return user.shopping_chart.filter(receipe=obj).exists()
