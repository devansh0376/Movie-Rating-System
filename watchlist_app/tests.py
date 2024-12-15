from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):
    #we should login first 
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token =Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)

        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="http://www.Netflix.com")

    #but for access the streamplatform we need to login 
    def test_streamplatform_create(self):
        data={
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "http://www.Netflix.com"
        }
        response=self.client.post(reverse('streamplatform-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response=self.client.get(reverse('streamplatform-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response=self.client.get(reverse('streamplatform-detail', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="http://www.Netflix.com") # creating stream platform
        self.watchlist=models.Watchlist.objects.create(platform=self.stream,title="Example Watchlist", storyline="Example story",active=True) # creating watchlist

    def test_watchlist_create(self): #post request 
        data={
            "platform":self.stream,
            "title":"Example Movie",
            "storyline":"Example story",
            "active":True
        }
        response=self.client.post(reverse('movie_list'),data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_list(self): #get request 
        response=self.client.get(reverse('movie_list')) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_watchlist_ind(self): #access individual elements
        response=self.client.get(reverse('movie_detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(models.Watchlist.objects.get().title,'Example Watchlist')

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token.key)
        self.stream=models.StreamPlatform.objects.create(name="Netflix",about="#1 Streaming Platform",website="http://www.Netflix.com") # creating stream platform
        self.watchlist=models.Watchlist.objects.create(platform=self.stream,title="Example Watchlist", storyline="Example story",active=True) # creating watchlist
        self.movie=models.Movie.objects.create(watchlist=self.watchlist,title="Example Movie",storyline="Example story",active=True) # creating movie 

        def test_review_create(self):
            data={
                "review_user":self.user,
                "ratting":5,
                "description":"Great Movie!",
                "watchlist":self.watchlist,
                "active":True
            }

            response=self.client.post(reverse('review-create',args=(self.watchlist.id,)),data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)