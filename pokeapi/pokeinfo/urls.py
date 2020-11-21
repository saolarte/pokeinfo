from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<str:poke_name>', views.fetch, name="fetch"),
]
