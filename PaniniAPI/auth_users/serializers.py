from rest_framework import serializers
from urllib.parse import parse_qs
import hmac
import hashlib
import json
from django.conf import settings


# class LoginResponseSerializer(serializers.Serializer):
#     token = serializers.CharField(required=True)
#     user = TelegramUserSerializer()


class TelegramAuthSerializer(serializers.Serializer):
    initData = serializers.CharField(required=True)

    def validate(self, attrs):
        parsed_data, user_data, is_valid = self.parse_and_verify_init_data(attrs['initData'])
        if not is_valid:
            raise serializers.ValidationError("Подпись не совпала")
        attrs['parsed_data'] = parsed_data
        attrs['user_data'] = user_data
        return attrs

    @staticmethod
    def parse_and_verify_init_data(init_data_str):
        parsed_data = parse_qs(init_data_str)

        received_hash = parsed_data.get('hash', [''])[0]
        if not received_hash:
            return None, None, False

        data_pairs = []
        for key, values in parsed_data.items():
            if key != 'hash':
                for value in values:
                    data_pairs.append((key, value))

        data_pairs.sort(key=lambda x: x[0])

        check_data_string = '\n'.join([f"{key}={value}" for key, value in data_pairs])
        bot_token = settings.TELEGRAM_BOT_TOKEN

        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()

        expected_hash = hmac.new(
            secret_key,
            check_data_string.encode(),
            hashlib.sha256
        ).hexdigest()
        is_valid = hmac.compare_digest(expected_hash, received_hash)

        user_data = {}
        if 'user' in parsed_data:
            try:
                user_data = json.loads(parsed_data['user'][0])
            except (json.JSONDecodeError, IndexError):
                pass

        return parsed_data, user_data, is_valid