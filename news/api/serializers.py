from rest_framework import serializers
from news import models
from datetime import datetime
from django.utils.timesince import timesince
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AuthorSerilizer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Author
        fields = 'email',


class AuthorizateSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] =AuthorSerilizer(models.Author.objects.get(email=user)).data
        return data

class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной


    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        label="Пароль"

    )

    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.


    class Meta:
        model = models.Author
        # Перечислить все поля, которые могут быть включеWны в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = ['email', 'password']

    def create(self, validated_data):

        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
      
        return models.Author.objects.create_user(**validated_data)
        

class WeddingSerilizer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = models.Wedding
        fields = '__all__'



class WeddingNameSerilizer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    WeddingDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = models.WeddingName
        fields = '__all__'
