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
        received_hash = parsed_data.get('hash')[0]
        check_data = []
        for key in parsed_data.keys():
            if key != 'hash':
                check_data.append(parsed_data[key][0])
        check_data_string = '\n'.join(check_data)

        secret_key = hmac.new(
            "WebAppData".encode(),
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        expected_hash = hmac.new(
            secret_key,
            check_data_string.encode(),
            hashlib.sha256
        ).hexdigest()
        is_valid = expected_hash == received_hash
        user_data = {}
        if 'user' in parsed_data:
            user_data = json.loads(parsed_data['user'][0])
        return parsed_data, user_data, is_valid
