from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TelegramAuthSerializer
from rest_framework import status


class TelegramAuthView(APIView):
    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data['user_data']
            return Response({
                'token': 'token',
                'user': 'user'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
