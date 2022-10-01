import djoser.serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return user.following.filter(author=obj).exists()


class SignUpSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации новых пользователецй."""

    class Meta:
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

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
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SetPasswordSerializer(djoser.serializers.PasswordSerializer):
    """Сериализатор изменения пароля"""
    current_password = serializers.CharField(
        source='password',
        style={"input_type": "password"},
        required=True
    )
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)
        extra_kwargs = {'current_password': {'write_only': True}}

    def validate(self, data):
        user = self.context["request"].user
        data = super().validate(data)
        if data["current_password"] == user.password:
            return data
        else:
            raise serializers.ValidationError('Неверно указан текущий пароль')
