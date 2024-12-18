from django.shortcuts import get_object_or_404
from .models import DepositComment, DepositLike, SavingsComment, SavingsLike
from .models import Deposit, Savings
from .serializers import DepositSerializer, SavingsSerializer
from django.db.models import Count
#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

## 예금 상품 api
# 예금 상품 전체 조회
@api_view(['GET'])
def deposit_list(request):
    # 정렬 기준 확인
    sort_by = request.GET.get('sort', 'default')
    
    # 예금 상품과 좋아요 정보를 한 번에 조회
    query = Deposit.objects.annotate(
        like_count=Count('likes')
    )
    
    # 정렬 적용
    if sort_by == 'rate':
        query = query.order_by('-intr_rate') # 금리순
    elif sort_by == 'bank':
        query = query.order_by('kor_co_nm') # 은행명
    elif sort_by == 'likes':
        query = query.order_by('-like_count')  # 좋아요 많은 순
    else:
        query = query.order_by('id') # 좋아요
    
    serializer = DepositSerializer(query, many=True)
    data = serializer.data
    
    if request.user.is_authenticated:
        user_likes = set(DepositLike.objects.filter(
            user=request.user
        ).values_list('deposit_id', flat=True))
        
        for item in data:
            item['is_liked'] = item['id'] in user_likes
    else:
        for item in data:
            item['is_liked'] = False
    
    return Response(data)

# 예금 상품 상세 조회
@api_view(['GET'])
def deposit_detail(request, id):
    try:
        deposit = get_object_or_404(Deposit, id=id)
        # 좋아요 정보 추가
        is_liked = False
        if request.user.is_authenticated:
            is_liked = DepositLike.objects.filter(deposit=deposit, user=request.user).exists()
        like_count = deposit.likes.count()
        
        data = {
            'id': deposit.id,
            'kor_co_nm': deposit.kor_co_nm,
            'fin_prdt_nm': deposit.fin_prdt_nm,
            'join_way': deposit.join_way,
            'join_member': deposit.join_member,
            'join_price': deposit.join_price,
            'intr_rate_type': deposit.intr_rate_type,
            'intr_rate_type_nm': deposit.intr_rate_type_nm,
            'save_trm': deposit.save_trm,
            'intr_rate': deposit.intr_rate,
            'intr_rate2': deposit.intr_rate2,
            'age_range': deposit.age_range,
            'is_liked': is_liked,
            'like_count': like_count
        }
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=404)

## 적금 상품 api
# 적금 상품 전체 조회
@api_view(['GET'])
def savings_list(request):
    # 정렬 기준 확인
    sort_by = request.GET.get('sort', 'default')
    
    # 적금 상품과 좋아요 정보를 한 번에 조회
    query = Savings.objects.annotate(
        like_count=Count('likes')
    )
    
    # 정렬 적용
    if sort_by == 'rate':
        query = query.order_by('-intr_rate') # 금리순
    elif sort_by == 'bank':
        query = query.order_by('kor_co_nm') # 은행명
    elif sort_by == 'likes':
        query = query.order_by('-like_count')  # 좋아요 많은 순
    else:
        query = query.order_by('id') # 전체
    
    # 시리얼라이저로 데이터 변환
    serializer = SavingsSerializer(query, many=True)
    data = serializer.data
    
    # 로그인한 사용자의 좋아요 정보를 한 번에 조회
    if request.user.is_authenticated:
        user_likes = set(SavingsLike.objects.filter(
            user=request.user
        ).values_list('savings_id', flat=True))
        
        # 좋아요 정보 추가
        for item in data:
            item['is_liked'] = item['id'] in user_likes
    else:
        for item in data:
            item['is_liked'] = False
    
    return Response(data)

# 적금 상품 상세 조회
def savings_detail(request, id):
    saving = Savings.objects.get(id=id)
    data = {
        'id': saving.id,
        'kor_co_nm': saving.kor_co_nm,
        'fin_prdt_nm': saving.fin_prdt_nm,
        'join_way': saving.join_way,
        'join_member': saving.join_member,
        'etc_note': saving.etc_note,
        'intr_rate_type_nm': saving.intr_rate_type_nm,
        'rsrv_type_nm': saving.rsrv_type_nm,
        'save_trm': saving.save_trm,
        'intr_rate': saving.intr_rate,
        'intr_rate2': saving.intr_rate2,
        'age_range': saving.age_range,
        'join_price': saving.join_price
    }
    return JsonResponse(data)

# 예금 댓글 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_add_comment(request, deposit_id):
    try:
        deposit = Deposit.objects.get(id=deposit_id)
        comment = DepositComment.objects.create(
            deposit=deposit,
            user=request.user,
            content=request.data.get('content')
        )
        return Response({
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
# 예금 댓글 조회
@api_view(['GET'])
def deposit_get_comments(request, deposit_id):
    try:
        deposit = Deposit.objects.get(id=deposit_id)
        comments = DepositComment.objects.filter(deposit=deposit).order_by('-created_at')
        
        comment_list = [{
            'id': comment.id,
            'content': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        
        return Response(comment_list)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
# 예금 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deposit_delete_comment(request, deposit_id, comment_id):
    try:
        comment = DepositComment.objects.get(id=comment_id)
        if comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 삭제할 수 있습니다."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except DepositComment.DoesNotExist:
        return Response(
            {"error": "댓글을 찾을 수 없습니다."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"Unexpected error: {e}")  # 예상치 못한 오류 출력
        return Response(
            {"error": "서버 오류입니다."}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# 예금 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_toggle_like(request, deposit_id):
    try:
        deposit = Deposit.objects.get(id=deposit_id)
        like, created = DepositLike.objects.get_or_create(
            deposit=deposit,
            user=request.user
        )
        
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
            
        like_count = deposit.likes.count()
        
        return Response({
            'status': 'success',
            'is_liked': is_liked,
            'like_count': like_count
        })
    except Deposit.DoesNotExist:
        return Response(
            {'error': '예금 상품을 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


# 예금 좋아요 상태
@api_view(['GET'])
def deposit_get_like_status(request, deposit_id):
    try:
        deposit = get_object_or_404(Deposit, id=deposit_id)
        is_liked = False
        if request.user.is_authenticated:
            is_liked = DepositLike.objects.filter(deposit=deposit, user=request.user).exists()
        like_count = deposit.likes.count()
        return Response({
            'is_liked': is_liked, 
            'like_count': like_count
        })
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
## 적금
# 적금 댓글 추가
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def savings_add_comment(request, savings_id):
    savings = get_object_or_404(Savings, id=savings_id)
    comment = SavingsComment.objects.create(
        savings=savings,
        user=request.user,
        content=request.data.get('content')
    )
    return Response({
        'id': comment.id,
        'content': comment.content,
        'user': comment.user.username,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }, status=status.HTTP_201_CREATED)
    
    
# 적금 댓글 조회
@api_view(['GET'])
def savings_get_comments(request, savings_id):
    savings = get_object_or_404(Savings, id=savings_id)
    comments = SavingsComment.objects.filter(savings=savings).order_by('-created_at')
    comment_list = [{
        'id': comment.id,
        'content': comment.content,
        'user': comment.user.username,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for comment in comments]
    return Response(comment_list)

# 적금 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def savings_delete_comment(request, savings_id, comment_id):
    comment = get_object_or_404(SavingsComment, id=comment_id, savings_id=savings_id)
    if comment.user != request.user:
        return Response(
            {"error": "댓글 작성자만 삭제할 수 있습니다."}, 
            status=status.HTTP_403_FORBIDDEN
        )
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 적금 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def savings_toggle_like(request, savings_id):
    try:
        savings = get_object_or_404(Savings, id=savings_id)
        like, created = SavingsLike.objects.get_or_create(
            savings=savings,
            user=request.user
        )
        if not created:
            like.delete()
            is_liked = False
        else:
            is_liked = True
        like_count = savings.likes.count()
        return Response({
            'status': 'success',
            'is_liked': is_liked,
            'like_count': like_count
        })
    except Savings.DoesNotExist:
        return Response(
            {'error': '적금 상품을 찾을 수 없습니다.'}, 
            status=status.HTTP_404_NOT_FOUND
        )

# 적금 좋아요 상태
@api_view(['GET'])
def savings_get_like_status(request, savings_id):
    savings = get_object_or_404(Savings, id=savings_id)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = SavingsLike.objects.filter(savings=savings, user=request.user).exists()
    like_count = savings.likes.count()
    return Response({
        'is_liked': is_liked, 
        'like_count': like_count
    })