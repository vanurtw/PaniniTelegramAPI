from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PlayerSerializer, ClubSerializer
from rest_framework.response import Response
from .models import Player, Club
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status


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
        responses={
            200: serializer_class(),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=['Коллекция карточек']
    )
    def get(self, request, slug):
        players = Player.objects.filter(club__slug=slug)
        tg_user_players = request.user.profile.footballer_cards.values_list('player_id', flat=True)
        serializer = self.serializer_class(players, many=True, context={'tg_user_players': tg_user_players})
        return Response(serializer.data, status=status.HTTP_200_OK)


class FootballClubAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClubSerializer

    @swagger_auto_schema(
        operation_summary='Получить все футбольные клубы',
        operation_description='''
        Возвращает всю информацию о футбольных клубах.
        Доступно только для авторизованных пользователей.
        ''',
        responses={
            200: serializer_class(),
            401: openapi.Response(description='Пользователь не авторизован')
        },
        tags=["Футбольные клубы"]
    )
    def get(self, request):
        clubs = Club.objects.all()
        serializer = self.serializer_class(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
