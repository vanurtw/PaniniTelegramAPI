from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


class TelegramAuthView(APIView):
    def post(self, request):
        return Response("a")
