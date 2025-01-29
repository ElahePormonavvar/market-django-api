from rest_framework import generics
from .models import Brand,ProductGroup,Product,Feature,FeatureValue
from .serializer import (BrandSerializer,ProductGroupSerializer,ProductSerializer,
                         FeatureSerializer,FeatureValueSerializer)
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsPremiumUser
from rest_framework.views import APIView
from django.db.models import Count, Q
# ----------------------------------------------------------------------
class BrandCreateView(generics.CreateAPIView):
    permission_classes = [IsPremiumUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandListView(generics.ListAPIView):
    permission_classes = [IsPremiumUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
# ----------------------------------------------------------------------
class ProductGroupCreateView(generics.CreateAPIView):
    permission_classes = [IsPremiumUser]
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer

# ----------------------------------------------------------------------
class ProductCreateView(viewsets.ModelViewSet):
    permission_classes = [IsPremiumUser]
    queryset = Product.objects.none()  # هیچ کالایی به طور پیش‌فرض برنگردانیم

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()  # ذخیره محصول و دریافت شیء محصول
            return Response(
                {"message": "محصول با موفقیت ایجاد شد.", "data": ProductSerializer(product).data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "خطا در ایجاد محصول.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
# ------------------------------------------------------------------------
class ProductListView(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ------------------------------------------------------------------------
class FeatureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPremiumUser]
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer

# ------------------------------------------------------------------------
class FeatureValueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPremiumUser]
    queryset = FeatureValue.objects.all()
    serializer_class = FeatureValueSerializer

# ------------------------------------------------------------------------
class CheapestProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('price')[:5]
    serializer_class = ProductSerializer

# ------------------------------------------------------------------------
class LatestProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    serializer_class = ProductSerializer

# ------------------------------------------------------------------------
class CategoryPopularProductGroupsView(APIView):
    def get(self, request):
        product_groups = ProductGroup.objects.filter(Q(is_active=True)) \
                                             .annotate(count=Count('products_of_groups')) \
                                             .order_by('-count')
        serializer = ProductGroupSerializer(product_groups, many=True)
        return Response(serializer.data)
# ------------------------------------------------------------------------
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

