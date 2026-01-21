from rest_framework import serializers
from catalogue.models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'firstname', 'lastname']
