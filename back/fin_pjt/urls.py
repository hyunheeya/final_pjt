from django.contrib import admin
from django.urls import path, include
from recommend.views import deposit_list, savings_list, deposit_detail, savings_detail
from accounts.views import get_user_info
from products.views import deposit_add_comment, delete_comment, deposit_toggle_like, deposit_get_comments, deposit_get_like_status
from products.views import savings_add_comment, savings_toggle_like, savings_get_comments, savings_get_like_status

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
    path('api/deposit-products/<int:id>/', deposit_detail, name='deposit_detail'),
        # 적금
    path('api/savings-products/', savings_list, name='savings_list'),
    path('api/savings-products/<int:id>/', savings_detail, name='savings_detail'),
    ## products_api
        # 예금 상품 좋아요, 댓글
    path('api/deposit-products/<int:deposit_id>/comments/', deposit_get_comments, name='get_comments'),
    path('api/deposit-products/<int:deposit_id>/comment/add/', deposit_add_comment, name='add_comment'),
    path('api/deposit-products/<int:deposit_id>/like/',deposit_toggle_like, name='toggle_like'),
    path('api/deposit-products/<int:deposit_id>/like-status/',deposit_get_like_status, name='get_like_status'),
        # 적금 상품 좋아요, 댓글
    path('api/savings-products/<int:deposit_id>/comments/', savings_get_comments, name='get_comments'),
    path('api/savings-products/<int:deposit_id>/comment/add/', savings_add_comment, name='add_comment'),
    path('api/savings-products/<int:product_id>/comment/<int:comment_id>/delete/',delete_comment,name='delete_comment'),
    path('api/savings-products/<int:deposit_id>/like/',savings_toggle_like, name='toggle_like'),
    path('api/savings-products/<int:deposit_id>/like-status/',savings_get_like_status, name='get_like_status'),
]
