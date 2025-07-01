# backend/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdukHukumViewSet, LogUpdateViewSet, ChartDataView , DataPotensiViewSet
from .views import verify_token

router = DefaultRouter()
router.register(r'produk-hukum', ProdukHukumViewSet)
router.register(r'log-updates', LogUpdateViewSet, basename='logupdate')
router.register(r'data-potensi', DataPotensiViewSet, basename='data-potensi')

urlpatterns = [
    path('', include(router.urls)),
    path('chart-data/', ChartDataView.as_view(), name='chart-data'),
    path('verify-token/', verify_token),
]
