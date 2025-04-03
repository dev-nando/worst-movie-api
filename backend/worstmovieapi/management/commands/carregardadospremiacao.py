import csv
import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from worstmovieapi.models import Produtor, Estudio, Filme, Premio

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
                    Produtor.objects.get_or_create(nome=name.strip())[0] \
                        for name in re.split(r",\sand\s|,\s|\sand\s", reg_produtores)]
                
                # Estúdio
                reg_estudios = linha.get("studios")
                estudios = [
                    Estudio.objects.get_or_create(nome=name.strip())[0] \
                        for name in re.split(r",\sand\s|,\s|\sand\s", reg_estudios)]

                # Filme
                filme, _ = Filme.objects.get_or_create(nome=linha.get("title"))
                for es in estudios:
                    filme.estudio.add(es)
                for pro in produtores:
                    filme.produtor.add(pro)

                # Premio
                premio, _ = Premio.objects.get_or_create(ano=linha.get("year"))
                premio.concorrentes.add(filme)
                if linha.get("winner").lower() == "yes":
                    premio.ganhador = filme
                    premio.save()

        self.stdout.write(self.style.SUCCESS("Dados foram importados para o Banco de Dados!"))