from django.urls import path
from . import views

app_name = 'updater'

urlpatterns = [
    path("", views.update, name="update"),
]
