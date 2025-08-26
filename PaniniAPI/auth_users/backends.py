from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from PaniniAPI.settings import TOKEN_HEADER
from .models import Token
from rest_framework.validators import ValidationError


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.META.get('HTTP_AUTHORIZATION', None)
        if key:
            token_header, token_key = key.split()
            if token_header != TOKEN_HEADER:
                raise ValidationError("Неверный заголовок токена")
            try:
                token = Token.objects.get(key=token_key)
                return token.user_telegram, token.key
            except Exception as ex:
                raise ValidationError(ex)
        return None, None
