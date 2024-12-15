from django.shortcuts import render,get_object_or_404
from watchlist_app.models import *
from django.http import HttpResponse,JsonResponse
from watchlist_app.api.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics,mixins,viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from watchlist_app.api.permissions import *
from rest_framework.throttling import UserRateThrottle , AnonRateThrottle,ScopedRateThrottle
from watchlist_app.api.throtlling import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter,OrderingFilter
from watchlist_app.api.pagination import *
# Create your views here.

#CLASS BASE VIEW
#here we don't need to define decorators

# Generic class base view

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    #this will give current user 
    # def get_queryset(self):
    #     username=self.kwargs.get('username') 
    #     return Review.objects.filter(review_user__username=username)#this will filter review by current username
    
    def get_queryset(self):
        username=self.request.query_params.get('username',None)#insted of direcly mapping the value we map the paramaters
        return Review.objects.filter(review_user__username=username)#this will filter review by current username

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated] #only authenticated users can create review
    throttle_classes=[ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie=Watchlist.objects.get(pk=pk)

        user=self.request.user
        review_queryset=Review.objects.filter(review_user=user,watchlist=movie)
        
        if review_queryset.exists():
            raise ValidationError('User has already reviewed this movie')

        if movie.total_ratings==0:
            movie.average_rating=serializer.validated_data['rating']
        else:
            movie.average_rating=(movie.average_rating+serializer.validated_data['rating'])/2
        
        movie.total_ratings=movie.total_ratings+1

        movie.save() 

        serializer.save(watchlist=movie,review_user=user)

class ReviewList(generics.ListAPIView):
    #queryset=Review.objects.all() # here we are getting all reviews 
    #but we need specific stream platform reviews so we create get queryset method
    serializer_class = ReviewSerializer
    #permission_classes = [IsAuthenticated] #only authenticated users can see reviews
    #throttle_classes=[UserRateThrottle , AnonRateThrottle] 
    throttle_classes=[ReviewListThrottle,AnonRateThrottle]
    filter_backends =[DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)#coz se set related name as watchlist in serializer
# class ReviewList(generics.ListAPIView):
#     queryset=Review.objects.all() # here we are getting all reviews 
#     #but we need specific stream platform reviews so we create get queryset method
#     serializer_class = ReviewSerializer
#     permission_classes =[IsReviewUserOrReadOnly]
#     throttle_classes=[UserRateThrottle , AnonRateThrottle]
#     #permission_classes = [IsAuthenticated] #only authenticated users can see reviews

#     def get_queryset(self):
#         pk=self.kwargs.get('pk')
#         return Review.objects.filter(watchlist=pk)#coz se set related name as watchlist in serializer

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):#get put and delete review
    queryset=Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly] #only authenticated users can see reviews 
    #if we don;t want to make throttling.py
    throttle_classes=[ScopedRateThrottle]
    throttle_scope='review_detail'


#class using mixins 
# class ReviewDetails(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self,request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
class StreamPlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset=StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset=StreamPlatform.objects.all()
#         serializer=StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def retrieve(self, request, pk=None):
#         queryset=StreamPlatform.objects.all()
#         watchlist=get_object_or_404(queryset,pk=pk)
#         serializer=StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer=StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     def destroy(self, request, pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def update(self, request, pk):
#         platform=StreamPlatform.objects.get(pk=pk)
#         serializer=StreamPlatformSerializer(platform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request): #back to front
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        #serializer = StreamPlatformSerializer(platforms, many=True,context={'request': request}) #for the link 
        return Response(serializer.data)
    
    def post(self,request): #front to back
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(selt,request, pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error':'Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer= StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self,request, pk):
        platform=StreamPlatform.objects.get(pk=pk)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListGV(generics.ListAPIView):
    queryset =Watchlist.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCPagination 
    # filter_backends =[DjangoFilterBackend]
    # filterset_fields = ['title','platform__name']
    # filter_backends =[SearchFilter]
    # search_fields = ['title','platform__name']
    #for exaxt match user = before fields
    #search_fields = ['=title','platform__name']
    #for ordering 
    filter_backends =[OrderingFilter]
    ordering_fields=['average_rating']
    

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]#only admin can edit and everyone can get request 
    def get(self, request):
        movies = Watchlist.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]#only admin can edit and everyone can get request
    def get(self,request, pk):
        try:
            movie = Watchlist.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'Error':'Not Found'},status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie=Watchlist.objects.get(pk=pk)
        serializer=WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie=Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#FUNCTION BASE VIEW
#with serializer we map all things in another file
#The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to
#@api_view(['GET', 'POST']) we are accepting GET and POST 
#default there is get request and get means back to front 
#@api_view()

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET': #back to front
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)#our serializer will visit multiple objects and serialize(map) them
#         return Response(serializer.data)
    
#     #we get data from user now we create object using serializer using create method
#     if request.method == 'POST': #front to back
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()#save() will save data in database
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)



# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET': 
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'Error':'Movie Not Found'},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)#here we are serializing single object so we don't need many=True
#         return Response(serializer.data)

#     if request.method == 'PUT': #we are updating object 
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#     if request.method == 'DELETE':#we are deleting object
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


