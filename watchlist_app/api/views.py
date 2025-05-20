from calendar import error
from rest_framework import status, mixins
from django.core.serializers import serialize
from django.template.context_processors import request
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from watchlist_app.models import WatchList,StreamPlatform,Reviews
from watchlist_app.api.serializers import WatchListSerializer,StreamPlatformSerializer, ReviewSerializer
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets

from watchlist_app.api.permissions import ReviewUserOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise  ValidationError("You have already reviewed this movie")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]


'''class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ReviewList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''
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


'''class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(watchlist)
        return Response(serializer.data)'''

#the best of them all its the modelViewSet
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer