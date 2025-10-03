from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from .autocomplete_views import CategoryAutocomplete, SubcategoryAutocomplete
from .views import (
    StatusViewSet,
    OperationTypeViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    MoneyMovementViewSet
)

router = routers.DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'operation_types', OperationTypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'money_movements', MoneyMovementViewSet)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/', include(router.urls)),
    path('category-autocomplete/', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    path('subcategory-autocomplete/', SubcategoryAutocomplete.as_view(), name='subcategory-autocomplete'),
]
