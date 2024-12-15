from rest_framework import serializers
from watchlist_app.models import *
# Back to Front => serialization and front to back => Deserialization 

# serialization : Complex data => python native data => json    (Back to Front)
# Deserialization: json => Python native data => complex data  (front to back)
#before we have to map all things in views and then we sent this using contex={'id':id} like this  but now we map all thing in this serializer.py so we use it directly

class ReviewSerializer(serializers.ModelSerializer):
    review_user=serializers.StringRelatedField(read_only=True)  # here we are using StringRelatedField which is used for showing related fields in our serializer
    class Meta:
        model = Review
        exclude=('watchlist',)
        #fields = '__all__' 

class WatchListSerializer(serializers.ModelSerializer):
    #reviews=ReviewSerializer(many=True, read_only=True)  # many=True means this field can have many reviews associated with it and with read only=True means when we send post request we can not send reviews in post request
    platform= serializers.CharField(source='platform.name') #we have to display the platform name  platform --> name 
    class Meta:  # we are mapping all fields in our model to serializer
        model=Watchlist
        fields = '__all__'  # we want to serialize all fields automatically

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist= WatchListSerializer(many=True, read_only=True)  # many=True means this field can have many watchlist associated with it
    #watchlist=serializers.StringRelatedField(many=True)
    # watchlist=serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie_detail'
    # )

    #here we use watchlist coz we define related name as watchlist in models.py
    class Meta:
        model = StreamPlatform
        fields = '__all__' 



# #Model serializer 
# #here set of default fields are automatically included,a set of validaties are automatically included
# #we have .create() and.update() methods for creating and updating objects respectively
# class MovieSerializer(serializers.ModelSerializer):

#     len_name= serializers.SerializerMethodField()  # we calculate length of name field in our serializer

#     class Meta:  # we are mapping all fields in our model to serializer
#         model = Watchlist
#         #fields = ('id', 'name', 'description', 'active') # we only want to serialize these fields
#         fields = '__all__'  # we want to serialize all fields automatically
#         #exclude = ['name']  # we exclude name field from serialization
    
#     def get_len_name(self, obj):  # we define a method in serializer to calculate length of name
#         return len(obj.name)

#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description should not be same")
#         else:
#             return data

#     def validate_name(self, value): 
#         if len(value)<2:
#             raise serializers.ValidationError("Name is too sort")  # we can add some validation here like check if name length
#         else:
#             return value

#use of validators for validation
# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError("Name is too sort")  # we can add some validation here like check if name length

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True) #read only 
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField(max_length=200)
#     active = serializers.BooleanField()

#     def create(self, validated_data): #this method is called when we want to create a new object
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data): #this method is called when we want to update an existing object
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)

#         instance.save()
#         return instance
#     #this method is called when we are validating data 
#     #object level validation
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description should not be same")
    #     else:
    #         return data
#     # this is field level validation
    # def validate_name(self, value): 
    #     if len(value)<2:
    #         raise serializers.ValidationError("Name is too sort")  # we can add some validation here like check if name length
    #     else:
    #         return value