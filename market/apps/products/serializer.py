from rest_framework import serializers
from .models import Brand,ProductGroup,Product, Feature, Brand, FeatureValue

# -------------------------------------------------------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['brand_title', 'image_name', 'slug']

# ----------------------------------------------------------------------
# class ProductGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductGroup
#         fields = ['group_title', 'image_name', 'description', 'is_active', 'group_parent', 'register_date', 'published_date', 'update_date', 'slug']
#         read_only_fields = ['register_date', 'update_date']


class ProductGroupSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)  # نمایش فرزندها

    class Meta:
        model = ProductGroup
        fields = ['id', 'group_title', 'group_parent', 'groups']  # فقط فیلدهای لازم


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
class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['feature_name', 'product_group']

# ------------------------------------------------------------------------
class FeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureValue
        fields = ['value_title', 'feature']
       
# ------------------------------------------------------------------------

