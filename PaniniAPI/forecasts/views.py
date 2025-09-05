from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import ForecastsSerializer, UserForecastsSerializer
from .models import Forecasts
from django.db import IntegrityError
from rest_framework import status
from rest_framework.validators import ValidationError


class ForecastsReadAPIView(GenericAPIView):
    serializer_class = ForecastsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''
        Надо будет исключить прогнрозы на которые пользовательуже дал ответы
        '''
        data = Forecasts.objects.filter(is_active=True)
        serializer = self.serializer_class(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserForecastsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserForecastsSerializer

    def post(self, request):
        '''
        обавить проверку на то чтобы пользователь не мог ответить на прогноз на который он уже отвечал с новым ответом
        '''
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(profile_user=request.user.profile)
        except IntegrityError:
            return Response({"detail": "Пользователь уже ответил на этот прогноз"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
