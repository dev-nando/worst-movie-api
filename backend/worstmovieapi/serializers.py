from __future__ import annotations

from rest_framework import serializers
from worstmovieapi.models import Producer, Studio, Movie

class ProducerSerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Producer
        fields = ["name", "movies"]


class StudioSerializer(serializers.ModelSerializer):
    movies = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Studio
        fields = ["name", "movies"]


class MovieSerializer(serializers.ModelSerializer):
    producer = serializers.StringRelatedField(many=True)
    studio = serializers.StringRelatedField(many=True)

    class Meta:
        model = Movie
        fields = ["name", "producer", "studio"]

