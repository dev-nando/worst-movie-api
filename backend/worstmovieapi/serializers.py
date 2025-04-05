"""Serializers."""
from __future__ import annotations

from typing import ClassVar

from rest_framework import serializers

from worstmovieapi.models import Movie, Producer, Studio


class ProducerSerializer(serializers.ModelSerializer):
    """Serializador das informações dos Produtores.

    :param serializers: Serializador herdado.
    :type serializers: serializers.ModelSerializer
    """

    movies = serializers.StringRelatedField(many=True)

    class Meta:
        """Meta Info."""

        model = Producer
        fields: ClassVar[list[str]] = ["name", "movies"]


class StudioSerializer(serializers.ModelSerializer):
    """Serializador das informações dos Estúdios.

    :param serializers: Serializador herdado.
    :type serializers: serializers.ModelSerializer
    """

    movies = serializers.StringRelatedField(many=True)

    class Meta:
        """Meta Info."""

        model = Studio
        fields: ClassVar[list[str]] = ["name", "movies"]


class MovieSerializer(serializers.ModelSerializer):
    """Serializador das informações dos Filmes.

    :param serializers: Serializador herdado.
    :type serializers: serializers.ModelSerializer
    """

    producer = serializers.StringRelatedField(many=True)
    studio = serializers.StringRelatedField(many=True)

    class Meta:
        """Meta Info."""

        model = Movie
        fields: ClassVar[list[str]] = ["name", "producer", "studio"]

