from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

@api_view(['GET'])
@permission_classes([AllowAny])
def exchangerate(request, currency):
    try:
        # 요청에서 날짜 파라미터 가져오기
        search_date = request.GET.get('searchdate')
        
        if not search_date:
            search_date = datetime.now().strftime('%Y%m%d')
            
        # 디버깅용 로그
        print(f"Received search date: {search_date}")
        
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"        # today = datetime.now().strftime('%Y%m%d')
        # today = 20241120
        # today = 20241121
        # today = 20241122
        # today = 20241010

        params = {
            'authkey': settings.EXCHANGE_API_KEY,
            'searchdate': search_date,
            'data': 'AP01'
        }

        # 디버깅용 로그
        print(f"Currency requested: {currency}")
        print(f"API params: {params}")
        
        response = requests.get(
            url, 
            params=params,
            verify=False,
        )
        
        print(f"API response status: {response.status_code}")
        print(f"API response content: {response.text}")
        
        if response.status_code != 200:
            return Response(
                {'error': '한국수출입은행 API 서버 오류'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        exchange_data = response.json()
        
        # 환율 데이터가 비어있는 경우
        if not exchange_data:
            return Response(
                {'error': '해당 통화의 환율 정보가 없습니다'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 통화 검색 (대소문자 구분 없이)
        for item in exchange_data:
            if item.get('cur_unit').upper() == currency.upper():
                try:
                    # 쉼표 제거 후 float로 변환
                    rate = float(item['tts'].replace(',', ''))
                    return Response({'rate': rate})
                except (ValueError, KeyError) as e:
                    print(f"Rate conversion error: {str(e)}")
                    return Response(
                        {'error': '환율 데이터 변환 오류'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        return Response(
            {'error': '환율 데이터를 불러올 수 없습니다'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return Response(
            {'error': '서버 오류가 발생했습니다'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )