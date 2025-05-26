# otp/urls.py
from django.urls import path
from .views import login_with_otp, verify_otp

urlpatterns = [
    path('login-with-otp/', login_with_otp, name='login_with_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
]
