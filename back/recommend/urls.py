from django.urls import path
from . import views

app_name='recommend'
urlpatterns = [
    path('recommend_products/', views.recommend_products, name='recommend_products'),
]

