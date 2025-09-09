from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ForecastsSerializer, UserForecastsSerializer, UserMyForecastsReadSerializer
from .models import Forecasts, UserForecasts
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ForecastsReadAPIView(GenericAPIView):
    serializer_class = ForecastsSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение всех пргнозов, возвращаются только активные прогнозы",
        operation_description='''
        Получение всех пргнозов с вариантами ответов, возвращаются только активные прогнозы.
        Доступно только  для авторизованных пользователей.
        ''',
        responses={
            200: serializer_class(),
            401: openapi.Response(description="Пользователь не авторизован")
        },
        tags=["Прогнозы"]
    )
    def get(self, request):
        '''
        Надо будет исключить прогнрозы на которые пользовательуже дал ответы
        '''
        if request.query_params.get("completed", None):
            data = Forecasts.objects.filter(is_active=True, completed=False)
        else:
            data = Forecasts.objects.filter(is_active=True)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserForecastsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserForecastsSerializer

    @swagger_auto_schema(
        operation_summary="Получение прогнозов на которые отвечал пользователь",
        operation_description='''
        Получение прогнозов с ответами и его ответом помеченным как флаг - user_answer -  на которые отвечал пользователь.
        Доступно только для авторизованных пользователей.
        ''',
        responses={
            200: openapi.Response(
                description='Фарм начат',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="id записи"
                        ),
                        "date_creation": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            format=openapi.FORMAT_DATETIME,
                            description='Дата создания записи'
                        ),
                        "forecast": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={"title": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Заголовок прогноза'
                            ),
                                "is_active": openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Флаг активен ли прогноз'
                                ),
                                "date_creation": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    format=openapi.FORMAT_DATETIME,
                                    description='Дата создания прогноза'
                                ),
                                "answer_options": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "id": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description="id записи"
                                        ),
                                        "title": openapi.Schema(
                                            type=openapi.TYPE_STRING,
                                            description='Заголовок ответа'
                                        ),
                                        "correct": openapi.Schema(
                                            type=openapi.TYPE_BOOLEAN,
                                            description='Флаг правильного ответа'
                                        ),
                                        "user_answer": openapi.Schema(
                                            type=openapi.TYPE_BOOLEAN,
                                            description='Флаг ответа пользователя'
                                        ),
                                    }
                                )
                            }
                        ),

                    }
                )

            ),
            401: openapi.Response(description="Пользователь не авторизован")
        },
        tags=["Прогнозы"]
    )
    def get(self, request):
        '''
        Получение прогнозов на которые пользовотель отвечал  с его ответами
        '''
        queryset = request.user.profile.user_forecasts.all()
        serializer = UserMyForecastsReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Ответить на пргоноз',
        operation_description='Ответить на прогноз. Доступен только для авторизованных пользователей',
        responses={
            200: serializer_class(),
            400: openapi.Response(
                description='Ошибка валидации',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Ошибка валидации"),
                    }
                )
            ),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Прогнозы"]
    )
    def post(self, request):
        '''
        Добавить проверку на то чтобы пользователь не мог ответить на прогноз на который он уже отвечал с новым ответом
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(profile_user=request.user.profile)
        except IntegrityError:
            return Response({"detail": "Пользователь уже ответил на этот прогноз"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ForecastUserDetailAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserForecastsSerializer

    @swagger_auto_schema(
        operation_summary="Обновить ответ пользователя на прогноз",
        operation_description='''
        Обновить ответ пользователя на прогноз.
        Доступно только для авторизованыых пользователей.
        ''',
        responses={
            200: serializer_class(),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Объект не найден',
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Описание ошибки"
                    ),
                }
            ),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Прогнозы"]

    )
    def patch(self, request, pk):
        '''
        Обновить ответ пользователя на прогноз
        '''
        data = request.data
        instance = get_object_or_404(UserForecasts, profile_user=request.user.profile, forecast__id=pk)
        serializer = self.serializer_class(data=data, instance=instance, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
