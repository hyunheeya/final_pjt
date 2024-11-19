from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Deposit, Savings

# Create your views here.
class RecommendationView(APIView):
    def post(self, request):
        # 요청 데이터 추출
        product_type = request.data.get('product_type')  # "예금" or "적금"
        age_range = request.data.get('age_range')
        join_way = request.data.get('join_way')
        join_member = request.data.get('join_member')
        intr_rate_type = request.data.get('intr_rate_type')
        join_price = request.data.get('join_price')

        # 예금 또는 적금에 따른 추천 처리
        if product_type == "예금":
            # 첫 번째 DB에서 예금 추천
            recommendations = Deposit.objects.using('default').filter(
                age_range=age_range,
                join_way=join_way,
                join_member=join_member,
                intr_rate_type=intr_rate_type,
                join_price=join_price
            )
        elif product_type == "적금":
            # 두 번째 DB에서 적금 추천
            rsrv_type = request.data.get('rsrv_type')  # 적금에서만 사용
            recommendations = Savings.objects.using('secondary').filter(
                age_range=age_range,
                join_way=join_way,
                join_member=join_member,
                intr_rate_type=intr_rate_type,
                join_price=join_price,
                rsrv_type=rsrv_type
            )
        else:
            return Response({"error": "Invalid product_type"}, status=status.HTTP_400_BAD_REQUEST)

        # 추천 결과 생성
        if recommendations.exists():
            result = [{"name": rec.name, "interest_rate": rec.interest_rate} for rec in recommendations]
            return Response({"recommendations": result}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No matching recommendations found."}, status=status.HTTP_404_NOT_FOUND)
