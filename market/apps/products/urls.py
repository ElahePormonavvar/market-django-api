from django.urls import path, include
from rest_framework.routers import DefaultRouter
import apps.products.views as views
from .views import ProductCreateView,ProductListView

# -------------------------------------------------------------------
router = DefaultRouter()
router.register(r'products-list', ProductListView, basename='product-list')
router.register(r'products-create', ProductCreateView,basename='product-create')

app_name = "products"

urlpatterns = [
    path('', include(router.urls)),
    path('brand-create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('productgroup/create/', views.ProductGroupCreateView.as_view(), name='productgroup-create'),
]
