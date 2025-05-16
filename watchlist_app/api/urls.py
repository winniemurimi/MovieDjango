
from django.urls import path, include
from watchlist_app.api.views import watchlist, movie_details,  stream,  stream_details



urlpatterns = [
     path('list/', watchlist,name='movie-list' ),
     path('<int:pk>', movie_details, name = 'movie-detail'),
     path('stream/', stream, name = 'streams'),
     path('stream/<int:pk>', stream_details, name = 'detail')
]

