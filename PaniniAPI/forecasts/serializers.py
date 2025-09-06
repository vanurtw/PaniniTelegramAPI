from rest_framework import serializers
from .models import Forecasts, AnswerOption, UserForecasts


class AnswerOptionForecastUserMySerializer(serializers.ModelSerializer):
    user_answer = serializers.SerializerMethodField()

    def get_user_answer(self, instance):
        return True

    class Meta:
        model = AnswerOption
        fields = [
            'id',
            'title',
            'correct',
            'user_answer'
        ]


class ForecastsMySerializer(serializers.ModelSerializer):
    answer_options = serializers.SerializerMethodField()

    def get_answer_options(self, instance):
        serializer = AnswerOptionForecastUserMySerializer(instance.answer_options.all(), many=True)
        return serializer.data

    class Meta:
        model = Forecasts
        fields = [
            'id',
            'title',
            'is_active',
            'date_creation',
            'answer_options'

        ]


class UserMyForecastsReadSerializer(serializers.ModelSerializer):
    forecast = serializers.SerializerMethodField()

    def get_forecast(self, instance):
        serializer = ForecastsMySerializer(instance.forecast)
        return serializer.data

    class Meta:
        model = UserForecasts
        fields = [
            'id',
            'forecast',
            'date_creation',
        ]


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
