from calendar import error
from rest_framework import status
from django.core.serializers import serialize
from django.template.context_processors import request
from rest_framework.response import Response
from watchlist_app.models import WatchList,StreamPlatform
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def stream(request):
    if request.method == 'GET':
        streams = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(streams, many = True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return  Response(serializer.errors, status=400)
    return None


@api_view(['GET', 'PUT', 'DELETE'])
def stream_details(request, pk):
    if request.method == 'GET':
        streams = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streams)
        return Response(serializer.data)

    elif request.method == 'PUT':
        streams = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(streams, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        streams = StreamPlatform.objects.get(pk=pk)
        streams.delete()
        return Response(status=204)
    return None


@api_view(['GET','POST'])
def watchlist(request):
    if request.method == 'GET':
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  # Return 201 Created status
        else:
            return Response(serializer.errors, status=400)
    return None


@api_view(['GET','PUT','DELETE'])
def movie_details(request, pk):
    if request.method == 'GET':
        movie = WatchList.objects.get(pk =pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'PUT':
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        movie = WatchList.objects.get(pk =pk)
        movie.delete()
        return Response(status=204)
    return None