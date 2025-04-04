import csv
import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from worstmovieapi.models import Producer, Studio, Movie, Award

class Command(BaseCommand):
    help = 'Importa os dados da premiação para o banco de dados'

    def handle(self, *args, **kwargs):
        if not os.path.exists(settings.DADOS):
            self.stderr.write(f"Error: File '{settings.DADOS}' not found.")
            return

        with open(settings.DADOS, newline='', encoding='utf-8') as csvfile:

            leitor = csv.DictReader(csvfile, delimiter=";")

            for linha in leitor:

                # Produtores
                reg_produtores = linha.get("producers")
                produtores = [
                    Producer.objects.get_or_create(name=name.strip())[0] \
                        for name in re.split(r",\sand\s|,\s|\sand\s", reg_produtores)]
                
                # Estúdio
                reg_estudios = linha.get("studios")
                estudios = [
                    Studio.objects.get_or_create(name=name.strip())[0] \
                        for name in re.split(r",\sand\s|,\s|\sand\s", reg_estudios)]

                # Filme
                filme, _ = Movie.objects.get_or_create(name=linha.get("title"))
                for es in estudios:
                    filme.studio.add(es)
                for pro in produtores:
                    filme.producer.add(pro)

                # Premio
                premio, _ = Award.objects.get_or_create(year=linha.get("year"))
                premio.contestants.add(filme)
                if linha.get("winner").lower() == "yes":
                    premio.winner.add(filme)

        self.stdout.write(self.style.SUCCESS("Dados foram importados para o Banco de Dados!"))