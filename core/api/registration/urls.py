from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from core.api.views import (
            create_user_viewset,
            profil_view,
            edit_profil_view,
            show_senders,
            show_messages
        )

app_name = 'account'

urlpatterns = [
    # Registration:
    path('register/', create_user_viewset, name='RegistrationViewset'),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('profile/', profil_view, name='profil_view'),
    path('edit/', edit_profil_view, name='edit_profil_view'),
    path('inbox/', show_senders, name='show_senders'),
    path('messages/<int:id>', show_messages, name='show_messages'),
]
