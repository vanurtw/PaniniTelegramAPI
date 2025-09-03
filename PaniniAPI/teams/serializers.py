from rest_framework import serializers
from .models import Club, Player


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = [
            'id',
            'name',
            'founded',
            'slug'
        ]


class PlayerSerializer(serializers.ModelSerializer):
    in_stock = serializers.SerializerMethodField()

    def get_in_stock(self, instance):
        return instance.id in self.context.get('tg_user_players', [])

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
            'photo',
            'in_stock'
        ]
