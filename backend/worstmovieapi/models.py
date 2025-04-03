from django.db import models

class Produtor(models.Model):
    nome = models.CharField("Nome")

class Estudio(models.Model):
    nome = models.CharField("Nome")

class Filme(models.Model):
    nome = models.CharField("Nome")
    produtor = models.ManyToManyField(Produtor)
    estudio = models.ManyToManyField(Estudio)

class Premio(models.Model):
    ano = models.IntegerField("Ano")
    concorrentes = models.ManyToManyField(Filme)
    ganhador = models.ForeignKey(Filme, on_delete=models.DO_NOTHING, related_name="ganhador", null=True)

