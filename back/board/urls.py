from django.urls import path
from . import views

app_name='board'
urlpatterns = [
    path('/articles', views.articles, name='articles'),
]