from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import Event, UserProfile, Message



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
        userprofile = UserProfile(user=user, user_description="Modifie ton profil", city="Modifie ton profil")
        user.save()
        userprofile.save()
        return user

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'username')



class EventSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner_name')
    class Meta:
        model = Event
        fields = ('id', 'city', 'owner', 'event_name', 'event_description', 'date', 'time')
    def get_owner_name(self, Event):
        owner = Event.owner.username
        return owner


class ShowSendersSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField('get_senders_name')
    print("******************************************ID:", id)
    class Meta:
        model = Message
        fields = ('sender',)

    def get_senders_name(self, Message):
        userId = Message.get('sender')
        print("******************************************ID:", userId)
        userProfile = UserProfile.objects.get(id = Message.get('sender'))
        return (userId,userProfile.user.username)




class ShowMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('sender', )
