# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse
# from .models import Deposit, Savings

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def recommend_products(request):
#     user_answers = request.POST.dict()  # URL 인코딩된 데이터를 딕셔너리로 변환
#     print("Received user_answers:", user_answers)  # 요청 데이터 확인

#     product_type = user_answers.get("1")  # 상품 유형 가져오기

#     if not product_type:
#         return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

#     if product_type == "예금":
#         return recommend_deposit(user_answers)
#     elif product_type == "적금":
#         return recommend_savings(user_answers)
#     else:
#         return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)

# def parse_range(field_value):
#     """
#     문자열 범위를 [최소값, 최대값] 리스트로 변환
#     """
#     try:
#         min_val, max_val = map(int, field_value.split(","))
#         return min_val, max_val
#     except ValueError:
#         return None, None  # 필드 값이 비정상적일 경우 None 반환

# def filter_by_age_and_amount(products, user_answers):
#     """
#     나이와 금액 필터링 함수
#     """
#     # 나이 필터링
#     if "5" in user_answers:  # 나이가 전달된 경우
#         user_age = int(user_answers["5"])
#         filtered_products = []
#         for product in products:
#             min_age, max_age = parse_range(product.age_range)
#             if min_age is not None and max_age is not None:
#                 if min_age <= user_age <= max_age:
#                     filtered_products.append(product)
#         products = products.filter(id__in=[p.id for p in filtered_products])
#         print(products)

#     # 금액 필터링
#     if "6" in user_answers:  # 금액이 전달된 경우
#         user_amount = int(user_answers["6"])
#         filtered_products = []
#         for product in products:
#             min_price, max_price = parse_range(product.join_price)
#             if min_price is not None and max_price is not None:
#                 if min_price <= user_amount <= max_price:
#                     filtered_products.append(product)
#         products = products.filter(id__in=[p.id for p in filtered_products])
#         print(products)

#     return products

# def recommend_deposit(user_answers):
#     products = Deposit.objects.all()

#     # 가입 방식 필터링
#     if "2" in user_answers:
#         products = products.filter(join_way__icontains=user_answers["2"])

#     # 금리 유형 필터링
#     if "3" in user_answers:
#         rate_type_map = {"단리": "단리", "복리": "복리"}
#         rate_type = rate_type_map.get(user_answers["3"])
#         if rate_type:
#             products = products.filter(intr_rate_type_nm=rate_type)

#     # 저축 기간 필터링
#     if "4" in user_answers:
#         term_map = {"6개월 이하": 6, "6개월~1년": 12, "1년 이상": 13}
#         term = term_map.get(user_answers["4"])
#         if term == 6:
#             products = products.filter(save_trm__lte=6)
#         elif term == 12:
#             products = products.filter(save_trm__range=(7, 12))
#         elif term == 13:
#             products = products.filter(save_trm__gte=13)

#     # 나이와 금액 필터링
#     products = filter_by_age_and_amount(products, user_answers)

#     return generate_recommendations(products)

# def recommend_savings(user_answers):
#     products = Savings.objects.all()

#     # 가입 방식 필터링
#     if "2" in user_answers:
#         products = products.filter(join_way__icontains=user_answers["2"])
#         print(products)

#     # 금리 유형 필터링
#     if "3" in user_answers:
#         rate_type_map = {"단리": "단리", "복리": "복리"}
#         rate_type = rate_type_map.get(user_answers["3"])
#         if rate_type:
#             products = products.filter(intr_rate_type_nm=rate_type)

#     # 저축 기간 필터링
#     if "4" in user_answers:
#         term_map = {"6개월 이하": 6, "6개월~1년": 12, "1년 이상": 13}
#         term = term_map.get(user_answers["4"])
#         if term == 6:
#             products = products.filter(save_trm__lte=6)
#         elif term == 12:
#             products = products.filter(save_trm__range=(7, 12))
#         elif term == 13:
#             products = products.filter(save_trm__gte=13)

#     # 나이와 금액 필터링
#     products = filter_by_age_and_amount(products, user_answers)

#     return generate_recommendations(products)

# def generate_recommendations(products):
#     recommendations = products.order_by('-intr_rate')[:3]
#     result = [{"name": product.fin_prdt_nm, "interest_rate": product.intr_rate} for product in recommendations]
#     return JsonResponse({"recommendations": result}, status=200)

# def calculate_weight(product, user_answers):
#     """
#     사용자 답변과 상품의 속성을 비교하여 가중치를 계산
#     """
#     weight = 0

#     # 가입 방식 가중치
#     if "2" in user_answers and user_answers["2"] in product.join_way:
#         weight += 1

#     # 금리 유형 가중치
#     if "3" in user_answers and user_answers["3"] == product.intr_rate_type_nm:
#         weight += 1

#     # 저축 기간 가중치
#     if "4" in user_answers:
#         term_map = {"3개월": 3, "6개월~1년": 12, "1년 이상": 13}
#         user_term = term_map.get(user_answers["4"])
#         if user_term:
#             if user_term == 6 and product.save_trm <= 6:
#                 weight += 1
#             elif user_term == 12 and 7 <= product.save_trm <= 12:
#                 weight += 1
#             elif user_term == 13 and product.save_trm >= 13:
#                 weight += 1

#     # 나이 범위 가중치
#     if "5" in user_answers:
#         user_age = int(user_answers["5"])
#         min_age, max_age = parse_range(product.age_range)
#         if min_age is not None and max_age is not None:
#             if min_age <= user_age <= max_age:
#                 weight += 1

#     # 금액 범위 가중치
#     if "6" in user_answers:
#         user_amount = int(user_answers["6"])
#         min_price, max_price = parse_range(product.join_price)
#         if min_price is not None and max_price is not None:
#             if min_price <= user_amount <= max_price:
#                 weight += 1

#     return weight

# def generate_recommendations(products, user_answers):
#     """
#     가중치를 계산하여 정렬 후 상위 3개의 추천 상품 반환
#     """
#     # 상품별 가중치 계산
#     weighted_products = []
#     for product in products:
#         weight = calculate_weight(product, user_answers)
#         weighted_products.append({
#             "product": product,
#             "weight": weight
#         })

#     # 가중치로 정렬 (동일 가중치의 경우 intr_rate2로 정렬)
#     sorted_products = sorted(
#         weighted_products,
#         key=lambda x: (-x["weight"], -getattr(x["product"], "intr_rate2", 0))
#     )

#     # 상위 3개의 추천 상품 추출
#     recommendations = sorted_products[:3]
#     result = [
#         {
#             "name": rec["product"].fin_prdt_nm,
#             "interest_rate": rec["product"].intr_rate,
#             "weight": rec["weight"]
#         }
#         for rec in recommendations
#     ]

#     return JsonResponse({"recommendations": result}, status=200)

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse
# from .models import Deposit, Savings

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def recommend_products(request):
#     """
#     사용자 입력을 받아 예금 또는 적금 상품을 추천합니다.
#     """
#     user_answers = request.data  # JSON 데이터를 가져옴
#     print("Received user_answers:", user_answers)  # 요청 데이터 확인

#     # 첫 번째 질문에 따라 상품 유형 결정
#     product_type = user_answers.get("1")  # 상품 유형 가져오기

#     if not product_type:
#         return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

#     # 상품 유형에 따라 추천 로직 호출
#     if product_type == "예금":
#         return recommend_deposit(user_answers)
#     elif product_type == "적금":
#         return recommend_savings(user_answers)
#     else:
#         return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)


# def recommend_deposit(user_answers):
#     """
#     예금 상품 추천
#     """
#     products = Deposit.objects.all()

#     # 각 상품에 대한 가중치 계산 및 추천 결과 생성
#     return generate_recommendations(products, user_answers)


# def recommend_savings(user_answers):
#     """
#     적금 상품 추천
#     """
#     products = Savings.objects.all()

#     # 각 상품에 대한 가중치 계산 및 추천 결과 생성
#     return generate_recommendations(products, user_answers)


# def parse_range(field_value):
#     """
#     문자열 범위를 [최소값, 최대값] 리스트로 변환
#     """
#     try:
#         min_val, max_val = map(int, field_value.split(","))
#         return min_val, max_val
#     except ValueError:
#         return None, None  # 필드 값이 비정상적일 경우 None 반환


# def calculate_weight(product, user_answers):
#     """
#     사용자 답변과 상품의 속성을 비교하여 가중치를 계산
#     """
#     weight = 0

#     # 가입 방식 가중치
#     if "2" in user_answers and user_answers["2"] in product.join_way:
#         weight += 1

#     # 금리 유형 가중치
#     if "3" in user_answers and user_answers["3"] == product.intr_rate_type_nm:
#         weight += 1

#     # 저축 기간 가중치
#     if "4" in user_answers:
#         term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
#         user_term = term_map.get(user_answers["4"])
#         if user_term:
#             if user_term == product.save_trm:
#                 weight += 1

#     # 나이 범위 가중치
#     if "5" in user_answers:
#         user_age = int(user_answers["5"])
#         min_age, max_age = parse_range(product.age_range)
#         if min_age is not None and max_age is not None:
#             if min_age <= user_age <= max_age:
#                 weight += 1

#     # 금액 범위 가중치
#     if "6" in user_answers:
#         user_amount = int(user_answers["6"])
#         min_price, max_price = parse_range(product.join_price)
#         min_price *= 10000
#         max_price *= 10000
#         if min_price is not None and max_price is not None:
#             if min_price <= user_amount <= max_price:
#                 weight += 1

#     return weight


# def generate_recommendations(products, user_answers):
#     """
#     사용자가 선택한 조건에 맞는 상품만 필터링하여 가중치를 계산하고 추천합니다.
#     """
#     # 조건에 맞는 상품 필터링
#     filtered_products = products.filter(
#         join_way__icontains=user_answers.get("2", ""),
#         intr_rate_type_nm=user_answers.get("3", ""),
#         # save_trm__exact=get_term_from_answer(user_answers.get("4", ""))
#     )

#     # 상품별 가중치 계산
#     weighted_products = [
#         {
#             "product": product,
#             "weight": calculate_weight(product, user_answers)
#         }
#         for product in filtered_products
#     ]

#     # 가중치로 정렬 (동일 가중치의 경우 intr_rate2로 정렬)
#     sorted_products = sorted(
#         weighted_products,
#         key=lambda x: (-x["weight"], -getattr(x["product"], "intr_rate2", 0))
#     )

#     # 상위 3개의 추천 상품 추출
#     recommendations = sorted_products[:3]
#     result = [
#         {
#             "name": rec["product"].fin_prdt_nm,
#             "interest_rate": rec["product"].intr_rate,
#             "weight": rec["weight"]
#         }
#         for rec in recommendations
#     ]

#     return JsonResponse({"recommendations": result}, status=200)


# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse
# from .models import Deposit, Savings


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def recommend_products(request):
#     """
#     사용자 답변을 처리하여 각 질문마다 필터링된 상품의 가중치를 업데이트하고,
#     질문이 끝난 후 최종적으로 추천 상품을 반환합니다.
#     """
#     user_answers = request.data  # JSON 데이터를 가져옴
#     print("Received user_answers:", user_answers)  # 요청 데이터 확인

#     # 첫 번째 질문에 따라 상품 유형 결정
#     product_type = user_answers.get("1")  # 상품 유형 가져오기
#     if not product_type:
#         return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

#     # 상품 유형에 따른 초기 상품 쿼리셋 설정
#     if product_type == "예금":
#         products = Deposit.objects.all()
#     elif product_type == "적금":
#         products = Savings.objects.all()
#     else:
#         return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)

#     # 가중치 저장을 위한 딕셔너리 초기화
#     product_weights = {product.id: 0 for product in products}

#     # 각 질문에 따라 필터링하고 가중치를 업데이트
#     for question_id, answer in user_answers.items():
#         if question_id == "1":  # 첫 번째 질문은 상품 유형 결정
#             continue

#         # 답변에 따라 필터링된 상품 가져오기
#         filtered_products = filter_products(products, question_id, answer)

#         # 필터링된 상품의 가중치를 증가
#         for product in filtered_products:
#             product_weights[product.id] += 1

#     # 모든 질문이 끝난 후 상품 정렬
#     sorted_products = sort_products_by_weight(products, product_weights)

#     # 상위 3개의 추천 상품 반환
#     top3_products = sorted_products[:3]
#     recommendations = [
#         {
#             "name": product.fin_prdt_nm,
#             "interest_rate": product.intr_rate,
#             "weight": product_weights[product.id],
#         }
#         for product in top3_products
#     ]

#     return JsonResponse({"recommendations": recommendations}, status=200)


# def filter_products(products, question_id, answer):
#     """
#     주어진 질문 ID와 답변에 따라 상품을 필터링합니다.
#     """
#     if question_id == "2":  # 가입 방식
#         return products.filter(join_way__icontains=answer)

#     if question_id == "3":  # 금리 유형
#         return products.filter(intr_rate_type_nm=answer)

#     if question_id == "4":  # 저축 기간
#         term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
#         save_trm = term_map.get(answer)
#         return products.filter(save_trm=save_trm)

#     if question_id == "5":  # 나이
#         user_age = int(answer)
#         return products.filter(age_range__contains=user_age)

#     if question_id == "6":  # 금액
#         user_amount = int(answer)
#         return products.filter(join_price__lte=user_amount * 10000)

#     return products


# def sort_products_by_weight(products, product_weights):
#     """
#     상품을 가중치와 intr_rate2를 기준으로 정렬합니다.
#     """
#     # 상품을 리스트로 변환하여 정렬
#     product_list = list(products)
#     product_list.sort(
#         key=lambda product: (-product_weights[product.id], -getattr(product, "intr_rate2", 0))
#     )
#     return product_list



# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from django.http import JsonResponse
# from .models import Deposit, Savings

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def recommend_products(request):
#     """
#     사용자 답변을 처리하여 예금 또는 적금 상품을 추천합니다.
#     """
#     user_answers = request.data  # JSON 데이터를 가져옴
#     print("Received user_answers:", user_answers)  # 요청 데이터 확인

#     # 첫 번째 질문에 따라 상품 유형 결정
#     product_type = user_answers.get("1")  # 상품 유형 가져오기
#     if not product_type:
#         return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

#     # 상품 유형에 따라 다른 추천 로직 호출
#     if product_type == "예금":
#         return recommend_deposit(user_answers)
#     elif product_type == "적금":
#         return recommend_savings(user_answers)
#     else:
#         return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)


# def recommend_deposit(user_answers):
#     """
#     예금 상품 추천 로직
#     """
#     products = Deposit.objects.all()

#     # 가중치 저장용 딕셔너리 초기화
#     product_weights = {product.id: 0 for product in products}

#     # 예금 관련 질문 처리 및 가중치 계산
#     for question_id, answer in user_answers.items():
#         if question_id == "1":  # 첫 번째 질문(상품 유형)은 이미 처리됨
#             continue

#         # 예금 질문에 따른 상품 필터링 및 가중치 업데이트
#         filtered_products = filter_deposit_products(products, question_id, answer)
#         for product in filtered_products:
#             product_weights[product.id] += 1

#     # 정렬 및 상위 3개 상품 추출
#     sorted_products = sort_products_by_weight(products, product_weights)
#     return generate_recommendation_response(sorted_products, product_weights)


# def recommend_savings(user_answers):
#     """
#     적금 상품 추천 로직
#     """
#     products = Savings.objects.all()

#     # 가중치 저장용 딕셔너리 초기화
#     product_weights = {product.id: 0 for product in products}

#     # 적금 관련 질문 처리 및 가중치 계산
#     for question_id, answer in user_answers.items():
#         if question_id == "1":  # 첫 번째 질문(상품 유형)은 이미 처리됨
#             continue

#         # 적금 질문에 따른 상품 필터링 및 가중치 업데이트
#         filtered_products = filter_savings_products(products, question_id, answer)
#         for product in filtered_products:
#             product_weights[product.id] += 1

#     # 정렬 및 상위 3개 상품 추출
#     sorted_products = sort_products_by_weight(products, product_weights)
#     return generate_recommendation_response(sorted_products, product_weights)


# def filter_deposit_products(products, question_id, answer):
#     """
#     예금 상품 필터링 로직
#     """
#     if question_id == "2":  # 가입 방식
#         return products.filter(join_way__icontains=answer)

#     if question_id == "3":  # 금리 유형
#         return products.filter(intr_rate_type_nm=answer)

#     if question_id == "4":  # 저축 기간
#         term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
#         save_trm = term_map.get(answer)
#         return products.filter(save_trm=save_trm)

#     if question_id == "5":  # 나이
#         user_age = int(answer)
#         return products.filter(age_range__contains=user_age)

#     if question_id == "6":  # 금액
#         user_amount = int(answer)
#         return products.filter(join_price__lte=user_amount * 10000)

#     return products


# def filter_savings_products(products, question_id, answer):
#     """
#     적금 상품 필터링 로직
#     """
#     if question_id == "2":  # 가입 방식
#         return products.filter(join_way__icontains=answer)

#     if question_id == "3":  # 저축 유형
#         return products.filter(save_type__icontains=answer)

#     if question_id == "4":  # 금리 유형
#         return products.filter(intr_rate_type_nm=answer)

#     if question_id == "5":  # 저축 기간
#         term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
#         save_trm = term_map.get(answer)
#         return products.filter(save_trm=save_trm)

#     if question_id == "6":  # 나이
#         user_age = int(answer)
#         return products.filter(age_range__contains=user_age)

#     if question_id == "7":  # 금액
#         user_amount = int(answer)
#         return products.filter(join_price__lte=user_amount * 10000)

#     return products


# def sort_products_by_weight(products, product_weights):
#     """
#     상품을 가중치와 intr_rate2를 기준으로 정렬합니다.
#     """
#     product_list = list(products)
#     product_list.sort(
#         key=lambda product: (-product_weights[product.id], -getattr(product, "intr_rate2", 0))
#     )
#     return product_list


# def generate_recommendation_response(sorted_products, product_weights):
#     """
#     추천 상품 응답 생성
#     """
#     top3_products = sorted_products[:3]
#     recommendations = [
#         {
#             "name": product.fin_prdt_nm,
#             "interest_rate": product.intr_rate,
#             "weight": product_weights[product.id],
#         }
#         for product in top3_products
#     ]
#     return JsonResponse({"recommendations": recommendations}, status=200)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .models import Deposit, Savings
# 예적금 api
from django.db.models import Count, Min, Max
from django.shortcuts import get_object_or_404
from urllib.parse import unquote # 상품명 특수문자 처리
from .serializers import DepositSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_products(request):
    user_answers = request.data
    print("Received user_answers:", user_answers)

    product_type = user_answers.get("1")
    if not product_type:
        return JsonResponse({"error": "상품 유형을 선택해주세요."}, status=400)

    if product_type == "예금":
        return recommend_deposit(user_answers)
    elif product_type == "적금":
        return recommend_savings(user_answers)
    else:
        return JsonResponse({"error": "유효하지 않은 상품 유형입니다."}, status=400)

def recommend_deposit(user_answers):
    products = Deposit.objects.all()
    product_weights = {product.id: 0 for product in products}

    # 가입 방식 필터링
    if "2" in user_answers:
        filtered_products = products.filter(join_way__icontains=user_answers["2"])
        for product in filtered_products:
            product_weights[product.id] += 1

    # 금리 유형 필터링
    if "3" in user_answers:
        filtered_products = products.filter(intr_rate_type_nm=user_answers["3"])
        for product in filtered_products:
            product_weights[product.id] += 1

    # 저축 기간 필터링
    if "4" in user_answers:
        term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
        save_trm = term_map.get(user_answers["4"])
        if save_trm:
            filtered_products = products.filter(save_trm=save_trm)
            for product in filtered_products:
                product_weights[product.id] += 1

    # 나이 필터링
    if "5" in user_answers:
        user_age = int(user_answers["5"])
        filtered_products = [p for p in products if in_age_range(p.age_range, user_age)]
        for product in filtered_products:
            product_weights[product.id] += 1

    # 금액 필터링
    if "6" in user_answers:
        user_amount = int(user_answers["6"])
        filtered_products = [p for p in products if deposit_in_join_price_range(p.join_price, user_amount)]
        for product in filtered_products:
            product_weights[product.id] += 1

    # 가중치와 이자율로 정렬
    sorted_products = sorted(products, key=lambda p: (-product_weights[p.id], -p.intr_rate2))
    top3_products = sorted_products[:3]

    recommendations = [
        {
            "name": product.fin_prdt_nm,
            "interest_rate": product.intr_rate,
            "save_trm": product.save_trm,
            "weight": product_weights[product.id],
            "product_type": user_answers["1"],
            "fin_prdt_nm": product.fin_prdt_nm,
            "id": product.pk
        }
        for product in top3_products
    ]

    return JsonResponse({"recommendations": recommendations}, status=200)

def recommend_savings(user_answers):
    products = Savings.objects.all()
    product_weights = {product.id: 0 for product in products}

    # 가입 방식 필터링
    if "2" in user_answers:
        filtered_products = products.filter(join_way__icontains=user_answers["2"])
        for product in filtered_products:
            product_weights[product.id] += 1

    # 저축 유형 필터링
    if "7" in user_answers:
        filtered_products = products.filter(rsrv_type_nm=user_answers["7"])
        for product in filtered_products:
            product_weights[product.id] += 1

    # 금리 유형 필터링
    if "3" in user_answers:
        filtered_products = products.filter(intr_rate_type_nm=user_answers["3"])
        for product in filtered_products:
            product_weights[product.id] += 1

    # 저축 기간 필터링
    if "4" in user_answers:
        term_map = {"3개월": 3, "6개월": 6, "1년": 12, "2년": 24, "3년": 36}
        save_trm = term_map.get(user_answers["4"])
        if save_trm:
            filtered_products = products.filter(save_trm=save_trm)
            for product in filtered_products:
                product_weights[product.id] += 1

    # 나이 필터링
    if "5" in user_answers:
        user_age = int(user_answers["5"])
        filtered_products = [p for p in products if in_age_range(p.age_range, user_age)]
        for product in filtered_products:
            product_weights[product.id] += 1

    # 금액 필터링
    if "6" in user_answers:
        user_amount = int(user_answers["6"])
        filtered_products = [p for p in products if saving_in_join_price_range(p.join_price, user_amount)]
        for product in filtered_products:
            product_weights[product.id] += 1

    # 가중치와 이자율로 정렬
    sorted_products = sorted(products, key=lambda p: (-product_weights[p.id], -p.intr_rate2))
    top3_products = sorted_products[:3]

    recommendations = [
        {
            "name": product.fin_prdt_nm,
            "interest_rate": product.intr_rate,
            "save_trm": product.save_trm,
            "weight": product_weights[product.id],
            "product_type": user_answers["1"],
            "fin_prdt_nm": product.fin_prdt_nm,
            "id": product.pk
        }
        for product in top3_products
    ]

    return JsonResponse({"recommendations": recommendations}, status=200)

def in_age_range(age_range, user_age):
    min_age, max_age = map(int, age_range.split(', '))
    return min_age <= user_age <= max_age

def deposit_in_join_price_range(join_price, user_amount):
    min_price = join_price * 10000
    return min_price <= user_amount

def saving_in_join_price_range(join_price, user_amount):
    min_price, max_price = map(float, join_price.split(', '))
    min_price *= 10000
    max_price *= 10000
    return min_price <= user_amount <= max_price

## 예금 상품 api
# 예금 상품 전체 조회
# def deposit_list(request):
#     deposits = Deposit.objects.values('kor_co_nm', 'fin_prdt_nm').annotate(
#         min_intr_rate=Min('intr_rate'),
#         max_intr_rate=Max('intr_rate'),
#         min_save_trm=Min('save_trm'),
#         max_save_trm=Max('save_trm')
#     ).distinct()

#     result = []
#     for deposit in deposits:
#         result.append({
#             'kor_co_nm': deposit['kor_co_nm'],
#             'fin_prdt_nm': deposit['fin_prdt_nm'],
#             'min_intr_rate': deposit['min_intr_rate'],
#             'max_intr_rate': deposit['max_intr_rate'],
#             'min_save_trm': deposit['min_save_trm'],
#             'max_save_trm': deposit['max_save_trm'],
#         })

#     return JsonResponse(result, safe=False)

def deposit_list(request):
    deposits = Deposit.objects.all().values('id', 'kor_co_nm', 'fin_prdt_nm', 'intr_rate', 'save_trm')
    return JsonResponse(list(deposits), safe=False)

# 예금 상품 상세 조회
def deposit_detail(request, id):
    deposit = get_object_or_404(Deposit, id=id)
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
        'age_range': deposit.age_range
    }
    return JsonResponse(data)

# def deposit_detail(request, fin_prdt_nm):
#     # URL 디코딩 및 공백/특수문자 처리
#     decoded_name = unquote(fin_prdt_nm).strip()
    
#     deposit = Deposit.objects.filter(fin_prdt_nm=decoded_name).first()
#     if not deposit:
#         return JsonResponse({'error': '상품을 찾을 수 없습니다.'}, status=404)

#     rates = Deposit.objects.filter(fin_prdt_nm=decoded_name).values(
#         'save_trm', 'intr_rate', 'intr_rate2'
#     )

#     data = {
#         'kor_co_nm': deposit.kor_co_nm,
#         'fin_prdt_nm': deposit.fin_prdt_nm,
#         'join_way': deposit.join_way,
#         'join_member': deposit.join_member,
#         'join_price': deposit.join_price,
#         'intr_rate_type': deposit.intr_rate_type,
#         'intr_rate_type_nm': deposit.intr_rate_type_nm,
#         'save_trm_rates': list(rates)
#     }
#     return JsonResponse(data)


## 적금 상품 api
# 적금 상품 전체 조회
def savings_list(request):
    savings = Savings.objects.all().values('id', 'kor_co_nm', 'fin_prdt_nm', 'intr_rate', 'save_trm', 'rsrv_type_nm')
    return JsonResponse(list(savings), safe=False)
# def savings_list(request):
#     # 상품명과 적립방식으로 그룹화
#     savings = Savings.objects.values('kor_co_nm', 'fin_prdt_nm', 'rsrv_type_nm').annotate(
#         min_intr_rate=Min('intr_rate'),
#         max_intr_rate=Max('intr_rate'),
#         min_save_trm=Min('save_trm'),
#         max_save_trm=Max('save_trm')
#     ).distinct()

#     result = []
#     for saving in savings:
#         result.append({
#             'kor_co_nm': saving['kor_co_nm'],
#             'fin_prdt_nm': saving['fin_prdt_nm'],
#             'rsrv_type_nm': saving['rsrv_type_nm'],  # 적립 방식 추가
#             'min_intr_rate': saving['min_intr_rate'],
#             'max_intr_rate': saving['max_intr_rate'],
#             'min_save_trm': saving['min_save_trm'],
#             'max_save_trm': saving['max_save_trm'],
#         })

#     return JsonResponse(result, safe=False)

# 적금 상품 상세 조회
def savings_list(request):
    savings = Savings.objects.all().values('id', 'kor_co_nm', 'fin_prdt_nm', 'intr_rate', 'intr_rate2', 'save_trm', 'rsrv_type_nm')
    return JsonResponse(list(savings), safe=False)

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

# def savings_detail(request, fin_prdt_nm, rsrv_type_nm):
#     # 상품명과 적립방식으로 필터링
#     saving = Savings.objects.filter(
#         fin_prdt_nm=fin_prdt_nm,
#         rsrv_type_nm=rsrv_type_nm
#     ).first()

#     if not saving:
#         return JsonResponse({'error': '상품을 찾을 수 없습니다.'}, status=404)

#     # 동일 상품의 모든 금리 정보 조회
#     rates = Savings.objects.filter(
#         fin_prdt_nm=fin_prdt_nm,
#         rsrv_type_nm=rsrv_type_nm
#     ).values('save_trm', 'intr_rate', 'intr_rate2')

#     data = {
#         'kor_co_nm': saving.kor_co_nm,
#         'fin_prdt_nm': saving.fin_prdt_nm,
#         'rsrv_type_nm': saving.rsrv_type_nm,
#         'join_way': saving.join_way,
#         'join_member': saving.join_member,
#         'join_price': saving.join_price,
#         'intr_rate_type': saving.intr_rate_type,
#         'intr_rate_type_nm': saving.intr_rate_type_nm,
#         'save_trm_rates': list(rates)
#     }
#     return JsonResponse(data)
