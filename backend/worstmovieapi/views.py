from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from worstmovieapi.models import Producer, Studio, Movie

from worstmovieapi.serializers import ProducerSerializer, MovieSerializer, StudioSerializer

@api_view(['GET'])
def getProducers(request):
    produtores = Producer.objects.all()
    serializer = ProducerSerializer(produtores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMinMaxProducerYearAwardInterval(request):
    produtores_premiados = {}
        
    for reg in Producer.objects.values_list("name", "movies__awards__year"):
        if reg[1]:
            produtores_premiados.setdefault(reg[0], []).append(reg[1])

    produtores_multi_premiados = {k: sorted(list(set(v))) for k, v in produtores_premiados.items() if len(v) > 1}

    intervalos_multipremiacoes = {}

    for produtor, anos_premiacoes in produtores_multi_premiados.items():
        for i in range(len(anos_premiacoes)-1):
            intervalo = anos_premiacoes[i+1] - anos_premiacoes[i]
            intervalos_multipremiacoes.setdefault(intervalo, []).append({
                "producer": produtor,
                "interval": intervalo,
                "previousWin": anos_premiacoes[i],
                "followingWin": anos_premiacoes[i+1]
                })

    min_max_interv_premiacoes = {
        "min": intervalos_multipremiacoes.get(min(list(intervalos_multipremiacoes.keys())))
        , "max": intervalos_multipremiacoes.get(max(list(intervalos_multipremiacoes.keys())))}
    
    return Response(min_max_interv_premiacoes)

@api_view(['GET'])
def getStudios(request):
    estudios = Studio.objects.all()
    serializer = StudioSerializer(estudios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMovies(request):
    filmes = Movie.objects.all()
    serializer = MovieSerializer(filmes, many=True)
    return Response(serializer.data)

