from django.urls import include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.urls import re_path, path
from .views import *

handler404 = 'core.views.view_404'


urlpatterns = [
    path('', home, name='index'),
    path('chercher/', search, name='search'),
    path('mes-evenements/', my_events, name='my_events'),
    path('mes-messages/<int:sender>/', show_messages, name='show_messages'),
    path('inbox/', show_senders, name='show_senders'),
    path('creer-evenement/', create_event, name='create_event'),
    path('envoyer-message/?sender=<sender>&receiver=<receiver>/', send_message, name='send_message'),
    path('chercher-evenement/', search_event, name='search_event'),
    path('register/', create_user, name='create_user'),
    path('mon-profil/', profile, name='profile'),
    path('profil/<int:id>/', visit_profile, name='visit_profile'),
    path('apply/<int:id>/', apply, name='apply'),
    path('valider/<int:id>/', validate, name='validate'),
    path('accept/?guest_id=<guest_id>&event_id=<event_id>/', accept, name='accept'),
    path('mon-profil/edit/', edit_profile, name='edit_profile'),
    path('change-password/', change_password, name='change_password'),
]

urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
