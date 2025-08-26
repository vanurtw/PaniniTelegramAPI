from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TelegramAuthSerializer
from rest_framework import status
from users.models import TelegramUserModel
from django.shortcuts import get_object_or_404
from .models import Token


class TelegramAuthView(APIView):
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data['user_data']
            users_telegram = TelegramUserModel.objects.filter(username=user_data['username'])
            if not users_telegram.exists():
                user_telegram = TelegramUserModel.objects.create(
                    user_id=user_data['id'],
                    username=user_data['username'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
            else:
                user_telegram = users_telegram[0]
            token = Token.objects.create(user_telegram=user_telegram)
            return Response({
                'token': token.key,
                'user': user_telegram.id
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
