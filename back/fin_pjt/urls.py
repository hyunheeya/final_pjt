from django.contrib import admin
from django.urls import path, include
from recommend.views import deposit_list, savings_list, deposit_detail, savings_detail
from accounts.views import get_user_info

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('recommend/', include('recommend.urls')),
    ## account_api
    path('api/user-info/',get_user_info, name='user_info'),
    ## recommend_api
    # 예금
    path('api/deposit-products/', deposit_list, name='deposit_list'),
    path('api/deposit-products/<str:fin_prdt_nm>/', deposit_detail, name='deposit_detail'),
    path('api/savings-products/', savings_list, name='savings_list'),
    path('api/savings-products/<str:fin_prdt_nm>/', savings_detail, name='savings_detail'),
]
