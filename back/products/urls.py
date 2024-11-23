from django.urls import path
from .views import (
    deposit_list, deposit_detail,
    savings_list, savings_detail,
    deposit_add_comment, deposit_get_comments, deposit_delete_comment,
    deposit_toggle_like, deposit_get_like_status,
    savings_add_comment, savings_get_comments, savings_delete_comment,
    savings_toggle_like, savings_get_like_status, sorted_deposits,
    sorted_savings,
)

app_name = 'products'

urlpatterns = [
    # 예금 상품 리스트 및 상세
    path('deposit-products/', deposit_list, name='deposit_list'),
    path('deposit-products/<int:id>/', deposit_detail, name='deposit_detail'),
    path('deposit-products/sorted/', sorted_deposits, name='sorted_deposits'),

    # 적금 상품 리스트 및 상세
    path('savings-products/', savings_list, name='savings_list'),
    path('savings-products/<int:id>/', savings_detail, name='savings_detail'),
    path('savings-products/sorted/', sorted_savings, name='sorted_savings'),  # 적금 금리순 조회

    # 예금 상품 좋아요 및 댓글
    path('deposit-products/<int:deposit_id>/comments/', deposit_get_comments, name='deposit_get_comments'),
    path('deposit-products/<int:deposit_id>/comment/add/', deposit_add_comment, name='deposit_add_comment'),
    path('deposit-products/<int:deposit_id>/comment/<int:comment_id>/delete/', deposit_delete_comment, name='deposit_delete_comment'),
    path('deposit-products/<int:deposit_id>/like/', deposit_toggle_like, name='deposit_toggle_like'),
    path('deposit-products/<int:deposit_id>/like-status/', deposit_get_like_status, name='deposit_get_like_status'),

    # 적금 상품 좋아요 및 댓글
    path('savings-products/<int:savings_id>/comments/', savings_get_comments, name='savings_get_comments'),
    path('savings-products/<int:savings_id>/comment/add/', savings_add_comment, name='savings_add_comment'),
    path('savings-products/<int:savings_id>/comment/<int:comment_id>/delete/', savings_delete_comment, name='savings_delete_comment'),
    path('savings-products/<int:savings_id>/like/', savings_toggle_like, name='savings_toggle_like'),
    path('savings-products/<int:savings_id>/like-status/', savings_get_like_status, name='savings_get_like_status'),
]
