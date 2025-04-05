"""Comando que carrega os dados do arquivo para o banco de dados."""
import csv
import re
from logging import getLogger
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from worstmovieapi.models import Award, Movie, Producer, Studio

logger = getLogger("django")

class Command(BaseCommand):
    """Implementação do comando."""

    help = "Importa os dados da premiação para o banco de dados"

    def handle(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003, ARG002
        """Lógica do comando."""
        if not Path(settings.DADOS).exists():
            msg = f"Arquivo '{settings.DADOS}' nao encontrado!"
            raise FileNotFoundError(msg)

        logger.info("Iniciando carga")

        with Path(settings.DADOS).open("r", encoding="utf-8") as csvfile:

            leitor = csv.DictReader(csvfile, delimiter=";")

            msg = f" '- Identificadas {leitor.line_num} linhas"
            logger.info(msg)

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

                msg = f"   '- linha carregada: {list(linha.values())}"
                logger.info(msg)

        logger.info("Dados foram carregados para o Banco de Dados!")

