"""Views."""
from urllib.request import Request

from rest_framework.decorators import api_view
from rest_framework.response import Response

from worstmovieapi.models import Movie, Producer, Studio
from worstmovieapi.serializers import (
    MovieSerializer,
    ProducerSerializer,
    StudioSerializer,
)


@api_view(["GET"])
def getproducers(request:Request) -> Response:  # noqa: ARG001
    """View que retorna os produtores.

    :param request: Request recebido.
    :type request: Request
    :return: Dados serializados dos produtores.
    :rtype: Response
    """
    produtores = Producer.objects.all()
    serializer = ProducerSerializer(produtores, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getminmaxproduceryearawardinterval(request:Request) -> Response:  # noqa: ARG001
    """View que retorna os produtores menor e maior intervalo entre os prêmios.

    :param request: _description_
    :type request: Request
    :return: _description_
    :rtype: Response
    """
    produtores_premiados = {}

    for reg in Producer.objects.values_list("name", "movies__awards__year"):
        if reg[1]:
            produtores_premiados.setdefault(reg[0], []).append(reg[1])

    produtores_multi_premiados = {
        k: sorted(set(v)) for k, v in produtores_premiados.items() if len(v) > 1}

    intervalos_multipremiacoes = {}

    for produtor, anos_premiacoes in produtores_multi_premiados.items():
        for i in range(len(anos_premiacoes)-1):
            intervalo = anos_premiacoes[i+1] - anos_premiacoes[i]
            intervalos_multipremiacoes.setdefault(intervalo, []).append({
                "producer": produtor,
                "interval": intervalo,
                "previousWin": anos_premiacoes[i],
                "followingWin": anos_premiacoes[i+1]})

    min_max_interv_premiacoes = {
        "min": \
            intervalos_multipremiacoes.get(min(list(intervalos_multipremiacoes.keys())))
        , "max": \
            intervalos_multipremiacoes.get(max(list(intervalos_multipremiacoes.keys())))}

    return Response(min_max_interv_premiacoes)

@api_view(["GET"])
def getstudios(request:Request) -> Response:  # noqa: ARG001
    """View que retorna os estúdios.

    :param request: Request recebido.
    :type request: Request
    :return: Dados serializados dos estúdios.
    :rtype: Response
    """
    estudios = Studio.objects.all()
    serializer = StudioSerializer(estudios, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getmovies(request:Request) -> Response:  # noqa: ARG001
    """View que retorna os filmes.

    :param request: Request recebido.
    :type request: Request
    :return: Dados serializados dos filmes.
    :rtype: Response
    """
    filmes = Movie.objects.all()
    serializer = MovieSerializer(filmes, many=True)
    return Response(serializer.data)

