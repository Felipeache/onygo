from django.urls import path


from core.api.views import EventViewset

app_name = 'core'

urlpatterns = [
    path('<int:id>/', EventViewset, name='EventViewset'),

]
