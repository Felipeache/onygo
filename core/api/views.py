from datetime import datetime
from core.models import Event, UserProfile, Message
from django.contrib.auth.models import User
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from itertools import chain
from rest_framework.permissions import IsAuthenticated
from core.api.serializers import (
    EventSerializer,
    CreateUserSerializer,
    ProfilSerializer,
    ShowSendersSerializer,
    ShowMessagesSerializer,
)


class EnventsListApi(ListAPIView):
    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("event_name", "event_description", "city")  # owner__username


def getUserFromToken(request):
    getUserId = Token.objects.get(
        key=request.META.get("HTTP_AUTHORIZATION").split()[1]
    ).user_id
    print("µµµµµµµ" * 40)
    print("getUserId", getUserId, flush=True)
    print("µµµµµµµ" * 40)
    return User.objects.get(id=getUserId)


@api_view(("POST",))
@permission_classes((IsAuthenticated,))
def send_message(request):
    getUser = getUserFromToken(request)
    me = UserProfile.objects.get(user_id=getUser.id)
    msg = Message(sender=me, receiver=getUser, text=request.POST.get("text"))
    msg.save()


@api_view(("GET",))
def show_senders(request):
    getUser = getUserFromToken(request)
    me = UserProfile.objects.get(user_id=getUser.id)
    senders = Message.objects.filter(receiver_id=me.id).values("sender").distinct()
    serializer = ShowSendersSerializer(senders, many=True)
    return Response(serializer.data)


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def show_messages(request, id):
    getUser = getUserFromToken(request)
    me = UserProfile.objects.get(user_id=getUser.id)
    received_msgs = (
        Message.objects.filter(sender=id, receiver=me.id)
        .distinct()
        .values("sent", "text", "sender")
        .order_by("sent")
    )
    sent_msgs = (
        Message.objects.filter(sender=me.id, receiver=id)
        .distinct()
        .values(
            "sent",
            "text",
            "sender",
        )
        .order_by("sent")
    )
    messages = sent_msgs | received_msgs
    serializer = ShowMessagesSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(
    [
        "GET",
    ]
)
@permission_classes((IsAuthenticated,))
def event_list_viewset(request):
    try:
        events = Event.objects.all()
        print("events", events, flush=True)
        print("33333333" * 50, flush=True)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(
    [
        "GET",
    ]
)
@permission_classes((IsAuthenticated,))
def get_event_viewset(request, id):
    try:
        events = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = EventSerializer(events)
    return Response(serializer.data)


@api_view(
    [
        "PUT",
    ]
)
@permission_classes((IsAuthenticated,))
def update_event_viewset(request, id):
    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if event.owner != user:
        return Response(
            {"Response": "Cet événement ne t'appartiens pas"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = EventSerializer(event, data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Evénement mis à jour"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Expected for an upcoming update
# @api_view(['DELETE',])
# def delete_event_viewset(request, id):
#     try:
#         events = Event.objects.get(id=id)
#     except Event.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     delete = events.delete()
#     data = {}
#     if delete:
#         data["success"] = "Evénement effacé"
#         return Response(data=data)
#     else:
#         data["failure"] = "Opps, Il y a eu une erreur"
#         return Response(serializers.errors, data=data)


@api_view(
    [
        "POST",
    ]
)
@permission_classes((IsAuthenticated,))
def create_event_viewset(request):
    getUserId = Token.objects.get(
        key=request.META.get("HTTP_AUTHORIZATION").split()[1]
    ).user_id
    getUserObj = User.objects.get(id=getUserId)
    ev = Event(owner=getUserObj)
    serializer = EventSerializer(ev, data=request.data)
    if serializer.is_valid():
        today = datetime.now().date()
        date_str = request.data.get("date")
        format_str = "%Y-%m-%d"
        date_obj = datetime.strptime(date_str, format_str)
        if date_obj.date() < today:
            raise serializers.ValidationError(
                {"date": "Il n'est pas possible de créer un événement dans le passé"}
            )
        crt_time = datetime.now().time()
        time_str = request.data.get("time")
        time_obj = datetime.strptime(time_str, "%H:%M")
        if time_obj.time() < crt_time and date_obj.date() <= today:
            raise serializers.ValidationError(
                {
                    "time": "Il n'est pas possible de \
                    créer un événement dans le passé"
                }
            )
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(
    [
        "POST",
    ]
)
def create_user_viewset(request):
    serializer = CreateUserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        user = serializer.save()
        Token.objects.create(user=User.objects.get(id=user.id))
        data["response"] = "Utilisateur crée"
        data["email"] = user.email
        data["username"] = user.username
        token = Token.objects.get(user=user).key
        data["token"] = token
        return Response({"Utilisateur créé": "ok", "token": token})
    else:
        data = serializer.errors
        return Response(data)


@api_view(["POST", "GET"])
@permission_classes((IsAuthenticated,))
def profil_view(request):
    try:
        user = getUserFromToken(request)
        # user=request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfilSerializer(user)
    return Response(serializer.data)


@api_view(
    [
        "PUT",
    ]
)
@permission_classes((IsAuthenticated,))
def edit_profil_view(request):
    try:
        user = request.user
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProfilSerializer(user, request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["response"] = "Ton profil a été modifié"
        return Response(data=data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
