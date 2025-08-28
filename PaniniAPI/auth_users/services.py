from users.models import TelegramUserModel
from .models import Token


class TelegramAuthService:
    @staticmethod
    def process_telegram_auth(user_data):
        user_telegram, created = TelegramUserModel.objects.get_or_create(
            user_id=user_data['id'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        token, _ = Token.objects.get_or_create(user_telegram=user_telegram)
        return {
            'token': token.key,
            'user_id': user_telegram.user_id,
        }
