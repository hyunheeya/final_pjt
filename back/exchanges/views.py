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
        # URL에서 직접 쿼리 파라미터 확인
        search_date = request.query_params.get('searchdate')
        # print(f"Received query parameter searchdate: {search_date}")
        
        if not search_date:
            search_date = datetime.now().strftime('%Y%m%d')
            # print(f"Using default date: {search_date}")
            
        try:
            datetime.strptime(search_date, '%Y%m%d')
        except ValueError:
            return Response(
                {'error': '잘못된 날짜 형식입니다'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 디버깅을 위한 로그 추가
        # print(f"Processing request for currency: {currency}, date: {search_date}")
        
        url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

        params = {
            'authkey': settings.EXCHANGE_API_KEY,
            'searchdate': search_date,
            'data': 'AP01'
        }

        # 디버깅용 로그
        # print(f"Currency requested: {currency}")
        # print(f"API params: {params}")
        
        response = requests.get(
            url, 
            params=params,
            verify=False,
        )
        
        # print(f"API response status: {response.status_code}")
        # print(f"API response content: {response.text}")
        
        if response.status_code != 200:
            return Response(
                {'error': '한국수출입은행 API 서버 오류'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        exchange_data = response.json()
        
        if not isinstance(exchange_data, list):
            return Response(
                {'error': '유효하지 않은 API 응답 형식'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        # 통화 검색 로직 개선
        currency_data = next(
            (item for item in exchange_data 
             if item.get('cur_unit', '').upper() == currency.upper()),
            None
        )
        
        if not currency_data:
            return Response(
                {'error': f'{search_date} 날짜의 {currency} 환율 정보가 없습니다'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # 환율 데이터 반환
        try:
            rate = float(currency_data['tts'].replace(',', ''))
            return Response({'rate': rate})
        except (ValueError, KeyError) as e:
            return Response(
                {'error': '환율 데이터 변환 오류'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        # print(f"Unexpected error: {str(e)}")
        return Response(
            {'error': '서버 오류가 발생했습니다'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )