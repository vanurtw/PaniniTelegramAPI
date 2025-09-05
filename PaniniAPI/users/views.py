from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import TelegramUserSerializer, FarmSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProfileTelegramUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramUserSerializer

    @swagger_auto_schema(
        operation_summary="Получение информации о пользователе",
        operation_description='''
        Получение информации о пользователе.
        Доступно только для аторизованных.
        ''',
        responses={
            200: serializer_class(),
            401: openapi.Response(description="Пользователь не авторизован")
        },
        tags=["Пользователи"]
    )
    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FarmStartUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Начать фарм",
        operation_description='''
        Начать фарм монет пользователя.
        Время фарма берется с профиля пользователя.
        Время начала фарма берется с времени сервера.
        Время окончания фарма = Время начала фарма + Время фарма.
        Доступно только для авторизованных пользователей.
        ''',
        responses={
            200: openapi.Response(
                description='Фарм начат',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The farm has started/Фарм начат"
                        ),
                        "end_datetime_farm": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_DATETIME,
                            description='DD.MM.YYYY HH:MM'
                        )
                    }
                )

            ),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Пользователи"]
    )
    def post(self, request):
        profile = request.user.profile
        profile.start_farm()
        return Response({
            "detail": "The farm has started",
            "end_datetime_farm": profile.end_datetime_farm.strftime("%d.%m.%Y %H:%M")
        }, status=status.HTTP_200_OK)


class FarmEndUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Прекратить фарм и забрать монеты",
        operation_description='''
        Прекращает фарм пользователя и если фарм заончен, то пополнит их колличество, 
        если фарм не был закончен, то вернет 0 coins.
        Доступно только для авторизованных пользователей.
        ''',
        responses={
            200: openapi.Response(
                description='The farm was assembled',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING,
                                                 description="The farm was assembled/Фарм закончен"),
                        'coins': openapi.Schema(type=openapi.TYPE_INTEGER, description="Сколько было нафармлено монет")
                    }
                )
            ),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Пользователи"]

    )
    def post(self, request):
        profile = request.user.profile
        coins = profile.collect_coins()
        return Response({
            "detail": "The farm was assembled",
            "coins": coins

        }, status=status.HTTP_200_OK)


class FarmAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FarmSerializer

    @swagger_auto_schema(
        operation_summary="Получить информацию а фарме пользователя",
        operation_description='''
        Возвращает информацию о фарме польователя: Время начала фарма, Время окончания фарма, Время фарма, Кол-во монет.
        Доступно только для авторизованных пользователей.
        ''',
        responses={
            200: serializer_class(),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Пользователи"]
    )
    def get(self, request):
        serializer = self.serializer_class(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
