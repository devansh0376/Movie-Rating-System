from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
# Create your models here.

class StreamPlatform(models.Model):
    name=models.CharField(max_length=50)
    about=models.CharField(max_length=200)
    website=models.URLField(max_length=100)

    def __str__(self):
        return self.name

class Watchlist(models.Model):
    title=models.CharField(max_length=50)
    storyline =models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist', null=True)#here one movie can have many platforms
    active=models.BooleanField(default=True)
    average_rating=models.FloatField(default=0)
    total_ratings=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user=models.ForeignKey (User,on_delete=models.CASCADE,related_name='review_user')#one user can have many reviews
    rating= models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.CharField(max_length=200,null=True)
    watchlist=models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='reviews')#one movie can have many reviews
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user )
 


# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField(max_length=200)
#     active=models.BooleanField(default=True)

#     def __str__(self):
#         return self.name