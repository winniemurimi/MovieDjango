from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import watchlist, movie_details, stream, stream_details, ReviewList, ReviewDetail, \
    ReviewCreate, StreamPlatformVS

router = routers.SimpleRouter()
router.register(r'stream', StreamPlatformVS, basename='stream_platform')

urlpatterns = [
    path('list/', watchlist, name='movie-list'),
    path('<int:pk>/', movie_details, name='movie-detail'),

    #path('stream/', stream, name = 'streams'),
    #path('stream/<int:pk>', stream_details, name = 'detail'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', stream_details, name='stream-detail'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail')
]

urlpatterns += router.urls
