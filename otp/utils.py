# otp/utils.py
import random
from django.core.mail import send_mail
import os

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}'
    from_email = os.getenv('EMAIL_HOST_USER', 'your-email@example.com')
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
