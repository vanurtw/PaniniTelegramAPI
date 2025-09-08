from rest_framework import serializers

from auth_users.serializers import TelegramAuthSerializer
from .models import ProfileTelegramUser, TelegramUserModel, UserFriends


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileTelegramUser
        fields = [
            'id',
            'coins',
            'is_farm',
            'start_datatime_farm',
            'end_datetime_farm',
        ]


class TelegramUserSerializer(serializers.ModelSerializer):
    profile = ProfileUserSerializer()

    class Meta:
        model = TelegramUserModel
        fields = [
            'id',
            'user_id',
            'username',
            'first_name',
            'last_name',
            'create_date',
            'profile'
        ]


class FarmSerializer(serializers.ModelSerializer):
    start_datatime_farm = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    end_datetime_farm = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = ProfileTelegramUser
        fields = [
            'is_farm',
            'start_datatime_farm',
            'end_datetime_farm',
            'time_farm',
            'coins'
        ]


class FriendSerializer(serializers.ModelSerializer):
    coins = serializers.CharField(source='profile.coins')

    class Meta:
        model = TelegramUserModel
        fields = [
            'user_id',
            'username',
            'coins'
        ]


class TelegramUserFriendsSerializer(TelegramAuthSerializer):
    '''
    Сериализатор который обрабатывет данные при добавление друга в список друзей
    '''
    telegram_user_id_friend = serializers.PrimaryKeyRelatedField(queryset=TelegramUserModel.objects.all())


class UserFriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriends
        fields = [
            'id',
            'user',
            'friend',
            'create_date'
        ]
