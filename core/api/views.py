from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from core.models import Event
from core.api.serializers import EventSerializer

@api_view(['GET',])
def EventViewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events)
    return Response(serializer.data)
