from django.contrib.auth.models import User 
from rest_framework import serializers

class RegistationSerialzers(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)#here write only means user can send infromation about password but can not read.
    class Meta:
        model = User
        fields = ['username','email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}#here password is inbuilt field so we have to manually set it readonly
    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError
            (
                {'error': 'password and password2 should be the same'}
            )

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError
            (
                {'error': 'email already exists'}
            )
        
        account=User(email=self.validated_data['email'],username=self.validated_data['username'],)
        account.set_password(password)
        account.save()

        return account