from django.urls import path, include
from rest_framework.routers import DefaultRouter
import apps.products.views as views

# --------------------------------------------------------------------------------------
router = DefaultRouter()
router.register(r'products-list', views.ProductListView, basename='product-list')
router.register(r'products-create', views.ProductCreateView,basename='product-create')
router.register(r'features', views.FeatureViewSet, basename='feature')
router.register(r'feature-values', views.FeatureValueViewSet, basename='feature-value')

app_name = "products"

urlpatterns = [
    path('', include(router.urls)),
    path('brand-create/', views.BrandCreateView.as_view(), name='brand-create'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('productgroup/create/', views.ProductGroupCreateView.as_view(), name='productgroup-create'),
    path('products-cheapest/', views.CheapestProductsView.as_view(), name='cheapest-products'),
    path('products-latest/', views.LatestProductsView.as_view(), name='latest-products'),
    path('products-category/', views.CategoryPopularProductGroupsView.as_view(), name='popular-product-groups'),
    path('products-detail/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
