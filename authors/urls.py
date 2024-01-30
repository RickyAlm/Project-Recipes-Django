from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('authors/', views.forms, name='authors'),
]
