from django.shortcuts import get_object_or_404
from .models import DepositComment, DepositLike, SavingsComment, SavingsLike
from recommend.models import Deposit, Savings
from django.contrib.auth.decorators import login_required
#
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# 예금 댓글 추가
@api_view(['POST'])
@login_required
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

# 예금 좋아요
@api_view(['POST'])
@login_required
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
# 댓글 추가
@api_view(['POST'])
@login_required
@permission_classes([IsAuthenticated])
def savings_add_comment(request, deposit_id):
    try:
        deposit = Savings.objects.get(id=deposit_id)
        comment = SavingsComment.objects.create(
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
    
# 적금 댓글 조회
@api_view(['GET'])
def savings_get_comments(request, deposit_id):
    try:
        deposit = Savings.objects.get(id=deposit_id)
        comments = SavingsComment.objects.filter(deposit=deposit).order_by('-created_at')
        
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
# 적금 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, product_id, comment_id):
    try:
        comment = SavingsComment.objects.get(id=comment_id)
        # 댓글 작성자와 요청자가 같은지 확인
        if comment.user != request.user:
            return Response(
                {"error": "댓글 작성자만 삭제할 수 있습니다."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except SavingsComment.DoesNotExist:
        return Response(
            {"error": "댓글을 찾을 수 없습니다."}, 
            status=status.HTTP_404_NOT_FOUND
        )

# 적금 좋아요
@api_view(['POST'])
@login_required
@permission_classes([IsAuthenticated])
def savings_toggle_like(request, deposit_id):
    try:
        deposit = Savings.objects.get(id=deposit_id)
        like, created = SavingsLike.objects.get_or_create(
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


# 적금 좋아요 상태
@api_view(['GET'])
def savings_get_like_status(request, deposit_id):
    try:
        deposit = get_object_or_404(Savings, id=deposit_id)
        is_liked = False
        if request.user.is_authenticated:
            is_liked = SavingsLike.objects.filter(deposit=deposit, user=request.user).exists()
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