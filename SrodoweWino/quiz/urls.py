from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('questions', views.quiz, name='questions'),
    path('add', views.add, name='add'),
    path('players', views.players, name='players'),
    path('scoreboard', views.scoreboard, name='scoreboard'),
]