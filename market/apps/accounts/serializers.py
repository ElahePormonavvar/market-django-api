from rest_framework import serializers
from django.contrib.auth import get_user_model
import utils
from django.utils.translation import gettext_lazy as _
# -------------------------------------------------------------------------------------------------------
CustomUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="تکرار رمز عبور")

    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'email', 'name', 'family', 'password', 'password2')

    def validate(self, attrs):
        password=attrs.get('password','')
        password2=attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError(_("رمزعبور و تکرار آن باید باهم برابر باشند"))
        return attrs

    def create(self, validated_data): 
        active_code = utils.creat_random_code(5)
        user = CustomUser.objects.create_user(
            mobile_number=validated_data['mobile_number'],
            email = validated_data.get('email', ''),
            name=validated_data['name'],
            family=validated_data['family'],
            active_code=active_code,
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        utils.send_sms(user.mobile_number,user.active_code)
        # print(f"کد فعال‌سازی: {active_code}")
        return user
    
# -----------------------------------------------------------------------------------------------------------------
class ActivateUserSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11, required=True)
    active_code = serializers.CharField(max_length=5, required=True)

    def validate(self, attrs):
        mobile_number = attrs.get('mobile_number')
        active_code = attrs.get('active_code')
        # بررسی وجود کاربر با شماره موبایل
        try:
            user = CustomUser.objects.get(mobile_number=mobile_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("کاربر با این شماره موبایل یافت نشد."))
        # بررسی کد فعال‌سازی
        if user.active_code != active_code:
            raise serializers.ValidationError(_("کد فعال‌سازی اشتباه است."))
        return attrs
    def save(self):
        mobile_number = self.validated_data['mobile_number']
        user = CustomUser.objects.get(mobile_number=mobile_number)
        user.is_active = True 
        user.active_code = '' 
        user.save()
        return user
    
# -----------------------------------------------------------------------------------------------------------------
class SendActivationCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(write_only=True)

    def validate_mobile_number(self, value):
        try:
            user = CustomUser.objects.get(mobile_number=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("کاربری با این شماره موبایل یافت نشد."))
        return value

    def create_reset_code(self, user):
        active_code = utils.creat_random_code(5) 
        user.active_code = active_code
        user.save()
        utils.send_sms(user.mobile_number,user.active_code)
        # print(f"کد فعال‌سازی: {active_code}")
        return active_code

    def save(self):
        mobile_number = self.validated_data['mobile_number']
        user = CustomUser.objects.get(mobile_number=mobile_number)
        self.create_reset_code(user)
        return user

# ------------------------------------------------------------------------------------------------------------------
class ChangePasswordSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=11)
    active_code = serializers.CharField(max_length=5)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        mobile_number = attrs['mobile_number']
        active_code = attrs['active_code']
        try:
            user = CustomUser.objects.get(mobile_number=mobile_number, active_code=active_code)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("کد فعال‌سازی یا شماره موبایل نادرست است."))
        return attrs

    def save(self):
        mobile_number = self.validated_data['mobile_number']
        new_password = self.validated_data['new_password']
        user = CustomUser.objects.get(mobile_number=mobile_number)
        user.set_password(new_password)  
        user.active_code = '' 
        user.save()

# ------------------------------------------------------------------------------------
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin']
        read_only_fields = ['id', 'is_admin']