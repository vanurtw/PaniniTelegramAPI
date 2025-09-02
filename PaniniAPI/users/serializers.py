from rest_framework import serializers
from .models import ProfileTelegramUser, TelegramUserModel


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTelegramUser
        fields = [
            'id',
            'coins',
            'is_farm',
        ]


class TelegramUserSerializer(serializers.ModelSerializer):
    profile = ProfileUserSerializer()

    class Meta:
        model = TelegramUserModel
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'create_date',
            'profile'
        ]
