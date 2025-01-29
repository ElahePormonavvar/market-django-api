from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,ActivateUserSerializer,SendActivationCodeSerializer,ChangePasswordSerializer,CustomUserSerializer)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.accounts.models import CustomUser
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# ---------------------------------------------------------------------------------------------------------------
class RegisterUser(GenericAPIView):
    serializer_class = RegisterSerializer 

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "کاربر با موفقیت ایجاد شد. کد فعال‌سازی به شماره موبایل شما ارسال شد."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ----------------------------------------------------------------------------------------------------------------
class ActivateUser(GenericAPIView):
    serializer_class = ActivateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # فعال‌سازی حساب کاربری
            user = serializer.save()
            return Response({
                "message": "حساب کاربری شما با موفقیت فعال شد. حالا می‌توانید وارد حساب خود شوید."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            "message": "ورود با موفقیت انجام شد",
            "user": {
                "mobile_number": user.mobile_number,
                "email": user.email,
                "name": user.name,
                "family": user.family,
            }
        })
        return data

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# --------------------------------------------------------------------------------------
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "توکن رفرش ارائه نشده است"}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()  # بی‌اعتبار کردن توکن

            return Response({"message": "با موفقیت خارج شدید"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "خطایی رخ داده است"}, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------
class SendActivationCodeView(APIView):
    def post(self, request):
        serializer = SendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کد فعال‌سازی به شماره موبایل ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# --------------------------------------------------------------------------------------------        
class PasswordRememberRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendActivationCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "کد فعال‌سازی ارسال شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ------------------------------------------------------------------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "رمز عبور با موفقیت تغییر کرد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------------------------------
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]