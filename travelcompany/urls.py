from django.urls import path

from . import views

urlpatterns = [
    path('', views.mhome, name='mhome')
]
