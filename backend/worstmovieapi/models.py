from django.db import models

class Producer(models.Model):
    name = models.CharField("Name")

    def __str__(self) -> str:
        return self.name


class Studio(models.Model):
    name = models.CharField("Name")

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    name = models.CharField("Name")
    producer = models.ManyToManyField(Producer, related_name='movies')
    studio = models.ManyToManyField(Studio, related_name='movies')

    def __str__(self) -> str:
        return self.name


class Award(models.Model):
    year = models.IntegerField("Year")
    contestants = models.ManyToManyField(Movie, related_name="contestant")
    winner = models.ManyToManyField(Movie, related_name="awards")

