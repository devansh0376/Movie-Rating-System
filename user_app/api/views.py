from rest_framework.decorators import api_view
from user_app.api.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from user_app import models

@api_view(['POST']) 
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST']) 
def registration_view(request):
    if request.method == 'POST':
        serializer=RegistationSerialzers(data=request.POST)
        data={}

        if serializer.is_valid():
            account=serializer.save()#when we call serializer twice it gives error
            data['response']="Registation successfull"
            data['username']=account.username
            data['email']=account.email
            # Generate token
            token=Token.objects.get(user=account).key
            data['token']=token
            #serializer.save()#when we call serializer twice it gives error
            # refresh=RefreshToken.for_user(account)
            # data['token']={
            #     'refresh':str(refresh),
            #     'access':str(refresh.access_token),
            # }
        else:
            data=serializer.errors

        return Response(data,status=status.HTTP_201_CREATED) #user name and email is send 
        