from rest_framework import generics
from .models import Brand,ProductGroup,Product
from .serializer import BrandSerializer,ProductGroupSerializer,ProductSerializer
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework import viewsets

# ----------------------------------------------------------------------
class BrandCreateView(generics.CreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

# ----------------------------------------------------------------------
class ProductGroupCreateView(generics.CreateAPIView):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer

# ----------------------------------------------------------------------
class ProductCreateView(viewsets.ModelViewSet):
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
