from rest_framework import serializers
from .models import Forecasts, AnswerOption, UserForecasts


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = [
            'id',
            'title',
            'correct'
        ]


class UserForecastsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserForecasts
        fields = [
            'id',
            'profile_user',
            'forecast',
            'answer_option',
            'date_creation'
        ]
        extra_kwargs = {"profile_user": {"read_only": True}}


class ForecastsSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, )

    class Meta:
        model = Forecasts
        fields = [
            'id',
            'title',
            'is_active',
            'date_creation',
            'answer_options'
        ]
