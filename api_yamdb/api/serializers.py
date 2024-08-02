from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта api/v1/auth/signup/"""

    class Meta:
        model = User
        fields = ('username', 'email')
        read_only_fields = ('password',)

    def create(self, validated_data):
        """Метод create создаёт нового пользователя."""
        username = validated_data.get('username')
        email = validated_data.get('email')
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        confirmation_code = self.send_code(email)
        user.confirmation_code = confirmation_code
        user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        """Метод .update() создаёт пользователю новый код."""
        confirmation_code = self.send_code(validated_data.get('email'))
        instance.confirmation_code = confirmation_code
        instance.save()
        return instance

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Unacceptable username')
        return value

    def send_code(self, recipient_email):
        """Отвечает за создание кода подтверждения и отправку писем.
        Функция randint создаёт 6-значный код.
        Отправка письма осуществляется на почту, которую указал пользователь
        """
        confirmation_code = randint(100000, 999999)
        message = f'Код для получения токена - {confirmation_code}'
        send_mail(
            'Код подтверждения',
            message,
            'from yamdb@mail.com',
            (recipient_email,),
            fail_silently=False
        )
        return confirmation_code


class GetTokenSerializer(TokenObtainSerializer):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            write_only=True
        )
        self.fields['confirmation_code'] = serializers.IntegerField()
        self.fields['password'] = serializers.CharField(read_only=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if data['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')
        data['token'] = str(self.get_token(user))
        return data

    @classmethod
    def get_token(cls, user):
        return AccessToken.for_user(user)
