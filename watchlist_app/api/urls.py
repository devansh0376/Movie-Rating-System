
from django.urls import path, include
from watchlist_app.models import *
from watchlist_app.api.views import *
from rest_framework.routers import DefaultRouter

router=DefaultRouter()  
router.register('stream', StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie_detail'),
    path('list/', WatchListAV.as_view(), name='movie_list'),
    path('list2/',WatchListGV.as_view(), name='watch_list'),

    path('',include(router.urls)),

    path('<int:pk>/review-create/',ReviewCreate.as_view(), name='review_create'),#we can create a review for particular movie
    path('<int:pk>/review/',ReviewList.as_view(), name='review_list'),#we can get all reviews of particular movie by its id
    path('review/<int:pk>/',ReviewDetails.as_view(), name='review_detail'),#filtering base on id
    #path('review/<str:username>/',UserReview.as_view(), name='user_review_detail'),#filtering base on username
    path('review/',UserReview.as_view(), name='user_review_detail'),#filtering base on username parameters

    
    # path('stream/', StreamPlatformAV.as_view(), name='movie_list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream_detail'),
    # path('review/',ReviewList.as_view(), name='review_list'),
    # path('review/<int:pk>',ReviewDetails.as_view(), name='review_detail'),
    
    # path('stream/<int:pk>/review-create',ReviewCreate.as_view(), name='review_create'),#we create a review for particular stream platform
    # path('stream/<int:pk>/review',ReviewList.as_view(), name='review_list'),#we get all reviews of particular stream platform
    # path('stream/review/<int:pk>',ReviewDetails.as_view(), name='review_detail'),#we get particular review of particular stream platform
    
    # # path('list/',movie_list,name='movie_list'),
    # path('<int:pk>',movie_details,name='movie_detail'),
]

