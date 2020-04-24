from django.urls import path


from core.api.views import (
            get_event_viewset,
            event_list_viewset,
            update_event_viewset,
            delete_event_viewset,
            create_event_viewset,
            create_user_viewset
        )

app_name = 'core'

urlpatterns = [
    # Registration:
    path('register/', create_user_viewset, name='create_user_viewset'),
    # Event model:
    path('', event_list_viewset, name='event_list_viewset'),
    path('<int:id>/', get_event_viewset, name='get_event_viewset'),
    path('<int:id>/update/', update_event_viewset, name='update_event_viewset'),
    path('<int:id>/delete/', delete_event_viewset, name='delete_event_viewset'),
    path('create/', create_event_viewset, name='create_event_viewset'),

]
