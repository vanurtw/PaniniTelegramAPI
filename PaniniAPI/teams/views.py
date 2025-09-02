from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PlayerSerializer
from rest_framework.response import Response
from .models import Player
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CollectionsAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlayerSerializer

    @swagger_auto_schema(
        operation_summary='Получение коллекции карточек футболистов',
        operation_description='''
        Получение карточек футболистов, с возможностью фильтрации по футбольным клубам.
        Доступно только для авторизованных пользователей.
        ''',
        manual_parameters=[
            openapi.Parameter(
                name='slug',
                in_=openapi.TYPE_STRING,
                description='slug футбольного клуба',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        tags=['Коллекция карточек']
    )
    def get(self, request, slug):
        players = Player.objects.filter(club__slug=slug)
        tg_user_players = request.user.profile.footballer_cards.values_list('player_id', flat=True)
        serializer = self.serializer_class(players, many=True, context={'tg_user_players': tg_user_players})
        return Response(serializer.data)
