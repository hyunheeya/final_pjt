from django.urls import path
from . import views

app_name='board'
urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_pk>/', views.article_detail, name='article_detail'),
]