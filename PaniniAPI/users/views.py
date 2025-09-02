from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelegramUserSerializer
from rest_framework.permissions import IsAuthenticated


class ProfileTelegramUser(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TelegramUserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        print(serializer)
        return Response(serializer.data)
