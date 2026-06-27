from django.urls import path, include
from .views import (
    CategoryViewSet,
    ProductViewSet,
    BrandViewSet,
    FirmViewSet,
    PurchasesViewSet,
    SalesViewSet,
    
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('product', ProductViewSet, basename='product')
router.register('brand', BrandViewSet, basename='brand')
router.register('firm', FirmViewSet, basename='firm')
router.register('purchases', PurchasesViewSet, basename='purchases')
router.register('sales', SalesViewSet, basename='sales')



urlpatterns = [
     path('router/', include(router.urls)),
]
