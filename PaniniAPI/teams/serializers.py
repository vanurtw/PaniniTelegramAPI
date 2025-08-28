from rest_framework import serializers
from .models import Club, Player


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id',
            'name',
            'founded'
        ]


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            'id',
            'name',
            'club',
            'position',
            'status_card',
            'number',
            'birth_date',
            'photo'
        ]


class CollectionsPlayersSerializer(serializers.Serializer):
    # player = serializers.CharField()
    club = ClubSerializer()
