from django.urls import path
from . import views

app_name='exchanges'
urlpatterns = [
    path('rates/<str:currency>/', views.exchangerate, name='exchangerate'),
]