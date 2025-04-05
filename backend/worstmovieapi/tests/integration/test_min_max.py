import tempfile

from django.conf import settings
from django.core.management import call_command
from django.urls import reverse

from rest_framework.test import APITestCase
from .test_cargadados import preencher_csv


class TestMinMax(APITestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self._ORIGINAL__DADOS = settings.DADOS
        settings.DADOS = f"{self.tempdir.name}/teste.csv"
        return super().setUp()
    
    def tearDown(self):
        settings.DADOS = self._ORIGINAL__DADOS
        return super().tearDown()

    def test_um_produtor(self):
        ano_1 = 1998
        ano_2 = 2002
        ano_sem_premio = 2007
        produtor = "Fulano"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {
                        "year":ano_1
                        , "title": "Filme 1"
                        , "studios": "Ghibli"
                        , "producers": produtor
                        , "winner": "yes"}
                    , {
                        "year":ano_2
                        , "title": "Filme 2"
                        , "studios": "Ghibli"
                        , "producers": produtor
                        , "winner": "yes"}
                    , {
                        "year":ano_sem_premio
                        , "title": "Filme 3"
                        , "studios": "Ghibli"
                        , "producers": produtor}])

        call_command("carregardadospremiacao")

        url = reverse("minmaxpyai")
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.data
            , {
                "min": [
                    {
                        "producer": produtor
                        , "interval": ano_2 - ano_1
                        , "previousWin": ano_1
                        , "followingWin": ano_2}]
                , "max": [
                    {
                        "producer": produtor
                        , "interval": ano_2 - ano_1
                        , "previousWin": ano_1
                        , "followingWin": ano_2}]})

    def test_dois_produtores(self):
        ano_1 = 1998
        ano_2 = 2002
        ano_3 = 2012
        produtor_min = "Fulano"
        produtor_max = "Alberto"
        with open(settings.DADOS, "w") as test_csv:
            preencher_csv(
                test_csv
                , [
                    {
                        "year":ano_1
                        , "title": "Filme 1"
                        , "studios": "Ghibli"
                        , "producers": produtor_min
                        , "winner": "yes"}
                    , {
                        "year":ano_2
                        , "title": "Filme 2"
                        , "studios": "Ghibli"
                        , "producers": f"{produtor_min} and {produtor_max}"
                        , "winner": "yes"}
                    , {
                        "year":ano_3
                        , "title": "Filme 3"
                        , "studios": "Ghibli"
                        , "producers": produtor_max
                        , "winner": "yes"}])

        call_command("carregardadospremiacao")

        url = reverse("minmaxpyai")
        response = self.client.get(url, format="json")
        self.assertEqual(
            response.data
            , {
                "min": [
                    {
                        "producer": produtor_min
                        , "interval": ano_2 - ano_1
                        , "previousWin": ano_1
                        , "followingWin": ano_2}]
                , "max": [
                    {
                        "producer": produtor_max
                        , "interval": ano_3 - ano_2
                        , "previousWin": ano_2
                        , "followingWin": ano_3}]})
