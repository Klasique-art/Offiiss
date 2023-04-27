from django.contrib import admin
from django.urls import path, include

from .views import chat_room



urlpatterns = [
path('room/<str:room_name>/',chat_room, name='chat-room'),

]

