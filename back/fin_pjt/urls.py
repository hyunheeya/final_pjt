"""
URL configuration for fin_pjt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from recommend.views import deposit_list, savings_list
from accounts.views import get_user_info

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('recommend/', include('recommend.urls')),
    ## account_api
    path('api/user-info/',get_user_info, name='user_info'),
    ## recommend_api
    path('api/deposit-products/', deposit_list, name='deposit_list'),
    path('api/savings-products/', savings_list, name='savings_list'),
]
