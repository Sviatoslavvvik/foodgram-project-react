from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Subscription

from recipes.models import Receipe  # isort:skip

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author_id=obj.id).exists()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации новых пользователецй."""

    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password')
        model = User
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'required': False},
                        'first_name': {'required': False},
                        'last_name': {'required': False}
                        }

    def validate(self, data):
        """Проверяем, что нельзя создать пользователя
         с существующим email и именем "me".
         """
        username = data['username']
        email = data['email']
        if username == 'me':
            raise serializers.ValidationError(
                'Нельзя создать пользователя с username = "me"'
            )
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                'Нельзя создать пользователя,'
                'email которого уже зарегистрирован'
            )
        return data

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SetPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор изменения пароля"""
    current_password = serializers.CharField(
        source='password',
        style={"input_type": "password"},
        required=True
    )
    new_password = serializers.CharField(required=True,
                                         style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('current_password', 'new_password')
        extra_kwargs = {
            'current_password': {'source': 'password', 'read_only': True},
            'new_password': {'write_only': True}
        }

    def validate(self, data):
        """Проверяем, пользователя по старому паролю
         новый пароль не может быть равен старому".
         """
        user = self.context.get("request").user

        if user.check_password(self.initial_data.get('new_password')):
            raise serializers.ValidationError('Новый пароль не должен'
                                              ' быть равным старому')

        if user.check_password(self.initial_data.get('current_password')):
            return data
        else:
            raise serializers.ValidationError('Неверно указан текущий пароль')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class RecipeShortDataSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор
    для отображения
    """
    class Meta:
        model = Receipe
        fields = (
            'id', 'name', 'image', 'cooking_time')


class SubscriptionsUserSerializer(serializers.ModelSerializer):
    """Сериализатор подписок пользователя (чтение)"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author_id=obj.id).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit_string = request.query_params.get(
            'recipes_limit'
        )
        if recipes_limit_string:
            recipes_limit = int(recipes_limit_string)
        else:
            recipes_limit = settings.RECIPE_AMOUNT_FOR_SUBCRIPTION
        recipes = obj.recipes.all().order_by('-pub_date')[:recipes_limit]

        return RecipeShortDataSerializer(
            recipes, many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class MakeSubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на запись"""

    id = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        source='author'
    )
    user = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('id', 'user'),
                message='Нельзя подписываться дважды!'
            )
        ]

    def validate(self, data):
        user = self.context.get('request').user
        if user == data.get('id'):
            raise serializers.ValidationError('Нельзя подписываться на себя!')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscriptionsUserSerializer(
            instance,
            context={'request': request}
        ).data
