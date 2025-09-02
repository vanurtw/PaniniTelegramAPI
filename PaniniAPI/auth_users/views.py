from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from users.serializers import TelegramUserSerializer
from .serializers import TelegramAuthSerializer, LoginResponseSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import TelegramAuthService


class TelegramAuthView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = TelegramAuthSerializer

    @swagger_auto_schema(
        operation_summary='Регистрация телеграм-пользователя',
        operation_description='''
        Регистрация телеграм-пользователя.
        В тело запроса передается InitData, возвращается token и информация о пользователе
        ''',
        request_body=TelegramAuthSerializer,
        responses={
            200: LoginResponseSerializer(),
            400: openapi.Response(description='Ошибка валидации'),

        },
        tags=['Авторизация']

    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data['user_data']
            auth_result = TelegramAuthService.process_telegram_auth(user_data)
            data_res = {
                'token': auth_result['token'],
                'user': auth_result['user']
            }
            serializer_response = LoginResponseSerializer(data_res)
            print(serializer_response.data)
            return Response(serializer_response.data)
            # return Response(data_res)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
