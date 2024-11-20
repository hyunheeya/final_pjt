from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Deposit, Savings

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user_answers = request.POST.dict()  # URL 인코딩된 데이터를 딕셔너리로 변환
    print("Received user_answers:", user_answers)  # 요청 데이터 확인

    product_type = user_answers.get("1")  # 상품 유형 가져오기

    if not product_type:
        return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

    if product_type == "예금":
        return recommend_deposit(user_answers)
    elif product_type == "적금":
        return recommend_savings(user_answers)
    else:
        return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)

def parse_range(field_value):
    """
    문자열 범위를 [최소값, 최대값] 리스트로 변환
    """
    try:
        min_val, max_val = map(int, field_value.split(","))
        return min_val, max_val
    except ValueError:
        return None, None  # 필드 값이 비정상적일 경우 None 반환

def filter_by_age_and_amount(products, user_answers):
    """
    나이와 금액 필터링 함수
    """
    # 나이 필터링
    if "5" in user_answers:  # 나이가 전달된 경우
        user_age = int(user_answers["5"])
        filtered_products = []
        for product in products:
            min_age, max_age = parse_range(product.age_range)
            if min_age is not None and max_age is not None:
                if min_age <= user_age <= max_age:
                    filtered_products.append(product)
        products = products.filter(id__in=[p.id for p in filtered_products])
        print(products)

    # 금액 필터링
    if "6" in user_answers:  # 금액이 전달된 경우
        user_amount = int(user_answers["6"])
        filtered_products = []
        for product in products:
            min_price, max_price = parse_range(product.join_price)
            if min_price is not None and max_price is not None:
                if min_price <= user_amount <= max_price:
                    filtered_products.append(product)
        products = products.filter(id__in=[p.id for p in filtered_products])
        print(products)

    return products

def recommend_deposit(user_answers):
    products = Deposit.objects.all()

    # 가입 방식 필터링
    if "2" in user_answers:
        products = products.filter(join_way__icontains=user_answers["2"])

    # 금리 유형 필터링
    if "3" in user_answers:
        rate_type_map = {"단리": "단리", "복리": "복리"}
        rate_type = rate_type_map.get(user_answers["3"])
        if rate_type:
            products = products.filter(intr_rate_type_nm=rate_type)

    # 저축 기간 필터링
    if "4" in user_answers:
        term_map = {"6개월 이하": 6, "6개월~1년": 12, "1년 이상": 13}
        term = term_map.get(user_answers["4"])
        if term == 6:
            products = products.filter(save_trm__lte=6)
        elif term == 12:
            products = products.filter(save_trm__range=(7, 12))
        elif term == 13:
            products = products.filter(save_trm__gte=13)

    # 나이와 금액 필터링
    products = filter_by_age_and_amount(products, user_answers)

    return generate_recommendations(products)

def recommend_savings(user_answers):
    products = Savings.objects.all()

    # 가입 방식 필터링
    if "2" in user_answers:
        products = products.filter(join_way__icontains=user_answers["2"])
        print(products)

    # 금리 유형 필터링
    if "3" in user_answers:
        rate_type_map = {"단리": "단리", "복리": "복리"}
        rate_type = rate_type_map.get(user_answers["3"])
        if rate_type:
            products = products.filter(intr_rate_type_nm=rate_type)

    # 저축 기간 필터링
    if "4" in user_answers:
        term_map = {"6개월 이하": 6, "6개월~1년": 12, "1년 이상": 13}
        term = term_map.get(user_answers["4"])
        if term == 6:
            products = products.filter(save_trm__lte=6)
        elif term == 12:
            products = products.filter(save_trm__range=(7, 12))
        elif term == 13:
            products = products.filter(save_trm__gte=13)

    # 나이와 금액 필터링
    products = filter_by_age_and_amount(products, user_answers)

    return generate_recommendations(products)

def generate_recommendations(products):
    recommendations = products.order_by('-intr_rate')[:3]
    result = [{"name": product.fin_prdt_nm, "interest_rate": product.intr_rate} for product in recommendations]
    return JsonResponse({"recommendations": result}, status=200)
