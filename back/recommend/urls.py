from django.urls import path
from . import views

app_name='recommend'
urlpatterns = [
    path('recommend_products/', views.recommend_products, name='recommend_products'),
]

# from django.urls import path
# from .views import deposit_list, savings_list, deposit_detail, savings_detail

# app_name = 'recommend'

# urlpatterns = [
#     # 예금 상품
#     path('deposit-products/', deposit_list, name='deposit_list'),
#     path('deposit-products/<int:id>/', deposit_detail, name='deposit_detail'),
    
#     # 적금 상품
#     path('savings-products/', savings_list, name='savings_list'),
#     path('savings-products/<int:id>/', savings_detail, name='savings_detail'),
# ]

