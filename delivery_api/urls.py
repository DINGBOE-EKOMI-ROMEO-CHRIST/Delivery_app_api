"""
URL configuration for delivery_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import salut

urlpatterns = [
    path('', salut, name='salut'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')), 
    path('api/', include('entreprises.urls')),
    path('api/', include('otp.urls')),
    path('api/', include('livreurs.urls')),
    path('api/', include('demande.urls')),
    path('api/', include('price.urls')),
    path('api/', include('delivery.urls')),
    path('api/', include('reclamation.urls')),
]
