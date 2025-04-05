import csv
import tempfile

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from worstmovieapi.models import Award, Movie, Producer, Studio


def preencher_csv(csvfile, linhas:list) -> None:
    writer = csv.DictWriter(
        csvfile, delimiter=";"
        , fieldnames=["year", "title", "studios", "producers", "winner"])
    writer.writeheader()
    for li in linhas:
        writer.writerow(li)


class TestCargaDados(TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self._ORIGINAL__DADOS = settings.DADOS
        settings.DADOS = f"{self.tempdir.name}/teste.csv"
        return super().setUp()

    def tearDown(self):
        settings.DADOS = self._ORIGINAL__DADOS
        return super().tearDown()

    def test_um_concorrente_ganhador(self):
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": "Filme 1", "studios": "Ghibli"
                     , "producers": "Miyazaki", "winner": "yes"}])

        call_command("carregardadospremiacao")

        self.assertEqual(Producer.objects.first().name, "Miyazaki")
        self.assertEqual(Studio.objects.first().name, "Ghibli")
        self.assertEqual(Movie.objects.first().name, "Filme 1")

        self.assertEqual(
            Movie.objects.first().producer.first(), Producer.objects.first())
        self.assertEqual(
            Movie.objects.first().studio.first(), Studio.objects.first())

        self.assertEqual(Producer.objects.first().movies.first(), Movie.objects.first())
        self.assertEqual(Studio.objects.first().movies.first(), Movie.objects.first())

        self.assertEqual(Award.objects.first().year, 2000)
        self.assertEqual(
            Award.objects.first().contestants.first(), Movie.objects.first())
        self.assertEqual(Award.objects.first().winner.first(), Movie.objects.first())

    def test_um_concorrente_perdedor(self):
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": "Filme 1"
                     , "studios": "Ghibli", "producers": "Miyazaki"}])

        call_command("carregardadospremiacao")

        self.assertEqual(Producer.objects.first().name, "Miyazaki")
        self.assertEqual(Studio.objects.first().name, "Ghibli")
        self.assertEqual(Movie.objects.first().name, "Filme 1")

        self.assertEqual(
            Movie.objects.first().producer.first(), Producer.objects.first())
        self.assertEqual(
            Movie.objects.first().studio.first(), Studio.objects.first())

        self.assertEqual(Producer.objects.first().movies.first(), Movie.objects.first())
        self.assertEqual(Studio.objects.first().movies.first(), Movie.objects.first())

        self.assertEqual(Award.objects.first().year, 2000)
        self.assertEqual(
            Award.objects.first().contestants.first(), Movie.objects.first())
        self.assertIsNone(Award.objects.first().winner.first())

    def test_um_estudio_com_dois_filmes_perdedores(self):
        filme_1 = "Filme 1"
        filme_2 = "Filme 2"
        estudio = "Ghibli"
        produtor_1 = "Miyazaki"
        produtor_2 = "Fulano"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": filme_1, "studios": estudio
                     , "producers": produtor_1}
                    , {"year":2001, "title": filme_2, "studios": estudio
                     , "producers": produtor_2}])

        call_command("carregardadospremiacao")

        self.assertEqual(len(Studio.objects.all()), 1)

        self.assertEqual(Movie.objects.get(name=filme_1).name, filme_1)
        self.assertEqual(Movie.objects.get(name=filme_2).name, filme_2)
        self.assertEqual(len(Movie.objects.all()), 2)

        self.assertEqual(len(Studio.objects.first().movies.exclude(awards=None)), 0)

    def test_um_estudio_com_dois_filmes_e_um_ganhador(self):
        filme_ganhador = "Filme 1"
        filme_perdedor = "Filme 2"
        estudio = "Ghibli"
        produtor_1 = "Miyazaki"
        produtor_2 = "Fulano"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": filme_ganhador, "studios": estudio
                     , "producers": produtor_1, "winner": "yes"}
                    , {"year":2001, "title": filme_perdedor, "studios": estudio
                     , "producers": produtor_2}])

        call_command("carregardadospremiacao")

        self.assertEqual(len(Studio.objects.all()), 1)
        self.assertEqual(Movie.objects.get(name=filme_ganhador).name, filme_ganhador)
        self.assertEqual(len(Studio.objects.first().movies.exclude(awards=None)), 1)
        self.assertEqual(
            Studio.objects.first().movies.exclude(awards=None)[0]
            , Movie.objects.get(name=filme_ganhador))

    def test_um_produtor_com_dois_filmes_perdedores(self):
        filme_1 = "Filme 1"
        filme_2 = "Filme 2"
        estudio_1 = "Ghibli"
        estudio_2 = "Ghibli 2"
        produtor_1 = "Miyazaki"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": filme_1, "studios": estudio_1
                     , "producers": produtor_1}
                    , {"year":2001, "title": filme_2, "studios": estudio_2
                     , "producers": produtor_1}])

        call_command("carregardadospremiacao")

        self.assertEqual(len(Producer.objects.all()), 1)

        self.assertEqual(Movie.objects.get(name=filme_1).name, filme_1)
        self.assertEqual(Movie.objects.get(name=filme_2).name, filme_2)
        self.assertEqual(len(Movie.objects.all()), 2)

        self.assertEqual(len(Producer.objects.first().movies.exclude(awards=None)), 0)

    def test_um_produtor_com_dois_filmes_e_um_ganhador(self):
        filme_ganhador = "Filme 1"
        filme_perdedor = "Filme 2"
        estudio_1 = "Ghibli"
        estudio_2 = "Ghibli 2"
        produtor = "Miyazaki"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": filme_ganhador, "studios": estudio_1
                     , "producers": produtor, "winner": "yes"}
                    , {"year":2001, "title": filme_perdedor, "studios": estudio_2
                     , "producers": produtor}])

        call_command("carregardadospremiacao")

        self.assertEqual(len(Producer.objects.all()), 1)
        self.assertEqual(Movie.objects.get(name=filme_ganhador).name, filme_ganhador)
        self.assertEqual(len(Producer.objects.first().movies.exclude(awards=None)), 1)
        self.assertEqual(
            Producer.objects.first().movies.exclude(awards=None)[0]
            , Movie.objects.get(name=filme_ganhador))

    def test_dois_produtores_do_mesmo_filme_ganhador_mas_um_tem_outro_filme_perdedor(self):
        filme_ganhador = "Filme 1"
        filme_perdedor = "Filme 2"
        estudio_1 = "Ghibli"
        estudio_2 = "Ghibli 2"
        produtor_1 = "Miyazaki"
        produtor_2 = "Fulano"

        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {"year":2000, "title": filme_ganhador, "studios": estudio_1
                     , "producers": f"{produtor_1} and {produtor_2}", "winner": "yes"}
                    , {"year":2001, "title": filme_perdedor, "studios": estudio_2
                     , "producers": produtor_2}])

        call_command("carregardadospremiacao")

        self.assertEqual(len(Producer.objects.all()), 2)
        self.assertEqual(len(Studio.objects.all()), 2)
        self.assertEqual(len(Movie.objects.all()), 2)
        self.assertEqual(len(Award.objects.all()), 2)

