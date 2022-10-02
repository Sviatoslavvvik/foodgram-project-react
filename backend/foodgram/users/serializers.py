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
        return user.follower.filter(author=obj).exists()


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


class SetPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор изменения пароля"""
    current_password = serializers.CharField(
        source='password',
        style={"input_type": "password"},
        required=True
    )
    new_password = serializers.CharField(required=True, source='password',
                                         style={"input_type": "password"})

    class Meta:
        model = User
        fields = ('current_password', 'new_password')
        extra_kwargs = {'current_password': {'write_only': True}}

    def validate(self, data):
        """Проверяем, пользователя по старому паролю
         новый пароль не может быть равен старому".
         """
        user = self.context.get("request").user

        if user.check_password(self.initial_data.get('new_password')):
            raise serializers.ValidationError('Новый пароль не должен'
                                              ' быть равным старому')

        if user.check_password(self.context.get('current_password')):
            return data
        else:
            raise serializers.ValidationError('Неверно указан текущий пароль')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
