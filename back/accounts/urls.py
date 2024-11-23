from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('user-info/',views.get_user_info, name='user_info'),
    path('liked-products/', views.user_liked_products, name='user-liked-products'),
    path('user-comments/', views.user_comments, name='user_comments'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change-password'),
]