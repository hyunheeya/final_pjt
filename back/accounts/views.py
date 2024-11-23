from products.models import Deposit,Savings
from products.serializers import DepositSerializer,SavingsSerializer
from django.db.models import Count

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 유저 정보
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'nickname': user.nickname,
    })

# 유저 좋아요
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_liked_products(request):
    user = request.user
    
    # 예금 좋아요 상품
    liked_deposits = Deposit.objects.filter(
        likes__user=user
    ).annotate(
        like_count=Count('likes')
    )
    
    # 적금 좋아요 상품
    liked_savings = Savings.objects.filter(
        likes__user=user
    ).annotate(
        like_count=Count('likes')
    )
        # 각각의 시리얼라이저로 데이터 변환
    deposit_serializer = DepositSerializer(liked_deposits, many=True)
    savings_serializer = SavingsSerializer(liked_savings, many=True)
    
    return Response({
        'deposits': deposit_serializer.data,
        'savings': savings_serializer.data
    })
