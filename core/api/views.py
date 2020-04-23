from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from core.models import Event, UserProfile
from core.api.serializers import EventSerializer, CreateUserSerializer

@api_view(['GET',])
def EventViewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events)
    return Response(serializer.data)


@api_view(['PUT',])
def UpdateViewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Evénement mis à jour"
        return Response(data=data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
def DeleteViewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    delete = events.delete()
    data = {}
    if delete:
        data["success"] = "Evénement effacé"
        return Response(data=data)
    else:
        data["failure"] = "Il y a eu une erreur"
        return Response(serializer.errors, data=data)

@api_view(['POST',])
def CreateViewset(request):
    user = User.objects.get(id=5)

    ev = Event(owner=user)
    serializer = EventSerializer(ev, data=request.data)
    if serializer.is_valid():
        date = request.data.get('date')
        if date < timezone.now():
            raise ValidationError ({'date':'date passé'})
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def RegistrationViewset(request):
    serializer = CreateUserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        data['response'] = 'Utilisateur crée'
        data['email'] = user.email
        data['username'] = user.username
    else:
        data = serializer.errors
    return Response(data)
