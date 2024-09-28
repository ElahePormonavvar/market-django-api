from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
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
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(_("رمزعبور و تکرار آن باید باهم برابر باشند"))
        return attrs

    def create(self, validated_data): 
        active_code = utils.create_random_code(5)
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
        # بجای پیام اینو نوشتم تا خرید سرویس پیامک
        print(f"کد فعال‌سازی: {active_code}")
        # ارسال کد فعال‌سازی
        # self.send_activation_code(user)
        return user
    
    #  def send_activation_code(self, user):
    #     # ارسال کد فعال‌سازی از طریق پیامک
    #     utils.send_sms(user.mobile_number, user.active_code)

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
        user.is_active = True  # فعال کردن کاربر
        user.active_code = ''  # پاک کردن کد فعال‌سازی بعد از استفاده
        user.save()
        return user
    
# -----------------------------------------------------------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = authenticate(mobile_number=data['mobile_number'], password=data['password'])
        if not user:
            raise serializers.ValidationError(_("شماره موبایل یا رمز عبور نادرست است"))
        if not user.is_active:
            raise serializers.ValidationError(_("حساب کاربری فعال نیست"))
        data['user'] = user
        return data
    
# ===================================================================================================================================================
# ===================================================================================================================================================
class SendActivationCodeSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(write_only=True)

    def validate_mobile_number(self, value):
        # بررسی وجود کاربر با این شماره موبایل
        try:
            user = CustomUser.objects.get(mobile_number=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("کاربری با این شماره موبایل یافت نشد."))
        return value

    def create_reset_code(self, user):
        active_code = utils.create_random_code(5) 
        user.active_code = active_code
        user.save()
        # اینجا می‌توانید از سرویس پیامکی برای ارسال کد استفاده کنید
        print(f"کد فعال‌سازی: {active_code}")
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
        user.active_code = ''  # پاک کردن کد فعال‌سازی پس از استفاده
        user.save()

# ------------------------------------------------------------------------------------
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin']
        read_only_fields = ['id', 'is_admin']