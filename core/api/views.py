from django.utils import timezone
from rest_framework import status
from rest_framework import serializers
from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from core.models import Event, UserProfile
from core.api.serializers import EventSerializer, CreateUserSerializer


@api_view(['GET',])
def event_list_viewset(request):
    try:
        events = Event.objects.all()
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET',])
def get_event_viewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events)
    return Response(serializer.data)


@api_view(['PUT',])
def update_event_viewset(request, id):
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
def delete_event_viewset(request, id):
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
        return Response(serializers.errors, data=data)

@api_view(['POST',])
def create_event_viewset(request):
    user = User.objects.get(id=5)

    ev = Event(owner=user)
    serializer = EventSerializer(ev, data=request.data)
    if serializer.is_valid():
        today = datetime.now().date()
        date_str = request.data.get('date')
        format_str = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, format_str)
        if date_obj.date() < today:
            raise serializers.ValidationError ({'date':'date passé'})
            return date == False

        crt_time = datetime.now().time()
        time_str = request.data.get('time')
        time_obj = datetime.strptime(time_str, '%H:%M')
        if time_obj.time() < crt_time and date_obj.date() <= today:
            raise serializers.ValidationError ({'time':'heure passé'})
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def create_user_viewset(request):
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
