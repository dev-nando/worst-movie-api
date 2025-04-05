"""Models."""
from django.db import models


class Producer(models.Model):
    """Model que representa os Produtores."""

    name = models.CharField("Name")

    def __str__(self) -> str:
        """Retorna self.name."""
        return self.name


class Studio(models.Model):
    """Model que representa os Estúdios."""

    name = models.CharField("Name")

    def __str__(self) -> str:
        """Retorna self.name."""
        return self.name


class Movie(models.Model):
    """Model que representa os Filmes."""

    name = models.CharField("Name")
    producer = models.ManyToManyField(Producer, related_name="movies")
    studio = models.ManyToManyField(Studio, related_name="movies")

    def __str__(self) -> str:
        """Retorna self.name."""
        return self.name


class Award(models.Model):
    """Model que representa as Premiações."""

    year = models.IntegerField("Year")
    contestants = models.ManyToManyField(Movie, related_name="contestant")
    winner = models.ManyToManyField(Movie, related_name="awards")

    def __str__(self) -> str:
        """Retorna self.year Award."""
        return f"{self.year} Award"

