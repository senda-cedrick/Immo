"""
URL configuration for immo_travel project.

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
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from app_base.views import home
from app_users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home,name='home')
    # Ajoutez cette ligne pour la racine :
    path('', include('app_base.urls')),
    path('user/', include('app_users.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/', include('knox.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='obtain_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    
]
