from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelegramUserSerializer
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
        return Response(serializer.data)
