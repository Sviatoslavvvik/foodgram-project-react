import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from recipes.models import IngredientInRecipe, Ingridient, Receipe, Tag
from rest_framework import serializers
from users.serializers import UserProfileSerializer

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
    """Сериализатор рецепта на чтение"""
    tags = TagSerializer(many=True, read_only=True)
    author = UserProfileSerializer(read_only=True)
    ingredients = IngridientInRecipeSerializer(
        many=True,
        source='ingridients_amounts',
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


class IngridientAmountWriteSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиента на запись"""
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            queryset=Ingridient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('amount', 'id')

    def validate_amount(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                'Количество не может быть меньше нуля'
            )
        return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта на запись"""
    ingredients = IngridientAmountWriteSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        model = Receipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time'
        )

    def create_bulk(self, recipe, ingredients_data):
        IngredientInRecipe.objects.bulk_create([IngredientInRecipe(
            ingridient=ingredient.get('ingredient'),
            receipe=recipe,
            amount=ingredient.get('amount')
        ) for ingredient in ingredients_data])

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Receipe.objects.create(author=request.user, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        self.create_bulk(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags_data)
        IngredientInRecipe.objects.filter(receipe=instance).delete()
        self.create_bulk(instance, ingredients_data)
        instance.save()
        return instance

    def validate(self, data):
        """Валидация ингредиентов и тэгов"""
        ingredients = []
        for ingredient in data.get('ingredients'):
            if ingredient.get('ingredient').id not in ingredients:
                ingredients.append(ingredient.get('ingredient').id)
            else:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!')
        tags = []
        for tag in data.get('tags'):
            if tag not in tags:
                tags.append(tag)
            else:
                raise serializers.ValidationError(
                    "Тэги не должны повторяться!"
                )
        return data

    def validate_cooking_time(self, data):
        """Проверка времени готовности"""
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше 0'
            )
        return data

    def to_representation(self, instance):
        data = ReceipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data
