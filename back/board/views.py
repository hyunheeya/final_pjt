from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Deposit, Savings
from products.models import DepositLike
from rest_framework.response import Response # DRF
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    pass