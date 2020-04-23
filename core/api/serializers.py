from rest_framework import serializers
from datetime import datetime
from django.contrib.auth.models import User

from core.models import Event, UserProfile



class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        #my_model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def save(self):
        user = User(
            username = self.validated_data['username'] ,
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            email = self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Les passwords ne correspondent pas'})
        user.set_password(password)
        user.save()
        return user



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    def save(self):
        ev = Event(
            date = self.validated_data['date'],
            time = self.validated_data['time']
        )
