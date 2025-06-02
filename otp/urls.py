# otp/urls.py
from django.urls import path
from .views import  verify_otp, refresh_otp

urlpatterns = [
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('refresh-otp/', refresh_otp, name='refresh_otp'),
]
