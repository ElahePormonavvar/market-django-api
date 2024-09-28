from django.contrib import admin
from django.urls import path
import apps.accounts.views as views

# -----------------------------------------------------------------------
app_name="accounts"

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('activate/',views.ActivateUser.as_view(), name='activate-user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('send_activation_code/', views.SendActivationCodeView.as_view(), name='send_activation_code'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password_reset/', views.PasswordRememberRequestView.as_view(), name='password_reset'),
]