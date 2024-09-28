from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (RegisterSerializer,LoginSerializer,ActivateUserSerializer,
                          SendActivationCodeSerializer,ChangePasswordSerializer,CustomUserSerializer)
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from apps.accounts.models import CustomUser

# ----------------------------------------------------------------------------------------------------------------
class RegisterUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "کاربر با موفقیت ایجاد شد. کد فعال‌سازی به شماره موبایل شما ارسال شد."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------------------------------------------------------------------------
class ActivateUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ActivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # حساب کاربر فعال می‌شود
            return Response({
                "message": "حساب کاربری شما با موفقیت فعال شد. حالا می‌توانید وارد حساب خود شوید."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------------------------------------------------
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "ورود با  موفقیت انجام شد", 
                "token": token.key,
                "user": {
                    "mobile_number": user.mobile_number,
                    "email": user.email,
                    "name": user.name,
                    "family": user.family,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # فقط کاربران لاگین شده می‌توانند از این ویو استفاده کنند

    def post(self, request):
        # توکن کاربر را پیدا کرده و حذف می‌کند
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # حذف توکن کاربر
            return Response({"message": "خروج با موفقیت انجام شد"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "خطا به هنگام خروج رخ داده"}, status=status.HTTP_400_BAD_REQUEST)
        

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