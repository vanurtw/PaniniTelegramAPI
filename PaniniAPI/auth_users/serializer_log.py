from rest_framework import serializers
from users.serializers import TelegramUserSerializer


class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    user = TelegramUserSerializer()
