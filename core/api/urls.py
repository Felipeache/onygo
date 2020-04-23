from django.urls import path


from core.api.views import EventViewset, UpdateViewset, DeleteViewset, CreateViewset, RegistrationViewset

app_name = 'core'

urlpatterns = [
    path('<int:id>/', EventViewset, name='EventViewset'),
    path('<int:id>/update/', UpdateViewset, name='UpdateViewset'),
    path('<int:id>/delete/', DeleteViewset, name='DeleteViewset'),
    path('create/', CreateViewset, name='CreateViewset'),
    path('', RegistrationViewset, name='RegistrationViewset'),

]
