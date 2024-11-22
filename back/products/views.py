from django.shortcuts import get_object_or_404
from .models import DepositComment, DepositLike, SavingsComment, SavingsLike
from .models import Deposit, Savings
#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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