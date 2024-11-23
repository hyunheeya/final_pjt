from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),

    # 앱별 URLs
    path('api/recommend/', include('recommend.urls')),  # 추천 API
    path('api/products/', include('products.urls')),  # 상품 관련 API
    path('api/accounts/', include('accounts.urls')),  # 사용자 정보
    path('api/board/', include('board.urls')),  # 게시판 관련

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)