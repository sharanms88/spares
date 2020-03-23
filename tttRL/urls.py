from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, kwargs={},name='create'),
    path('game/<str:game_id>/play', views.play, kwargs={}, name='play'),
]