from rest_framework import serializers
from .models import Brand,ProductGroup,Product, Feature, Brand

# -------------------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_title', 'image_name', 'slug']

# ----------------------------------------------------------------------
class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['group_title', 'image_name', 'description', 'is_active', 'group_parent', 'register_date', 'published_date', 'update_date', 'slug']
        read_only_fields = ['register_date', 'update_date']

# ------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    product_group = serializers.PrimaryKeyRelatedField(
        queryset=ProductGroup.objects.all(), many=True)
    features = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(), many=True)
    brand = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

# ------------------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # یا می‌توانید لیست فیلدهایی که می‌خواهید نشان دهید را مشخص کنید

