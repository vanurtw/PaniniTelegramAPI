from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TelegramAuthSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .services import TelegramAuthService


class TelegramAuthView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data['user_data']
            auth_result = TelegramAuthService.process_telegram_auth(user_data)
            return Response({
                'token': auth_result['token'],
                'user': auth_result['user_id']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAPIVIew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response("ok")
