from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from app_base.views import dashboard, GalleryView
from app_users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Page d'accueil publique -> galerie des logements disponibles
    path('', GalleryView.as_view(), name='home'),
    # Dashboard administrateur/utilisateurs (interface)
    path('dashboard/', dashboard, name='dashboard'),
    path('app/', include('app_base.urls')), # Les autres URLs de l'app sont préfixées par /app/
    path('paiements/', include('app_paiements.urls')), # URLs pour la gestion des paiements
    path('caisses/', include('app_caisse.urls')), # URLs pour la gestion de caisse
    path('user/', include('app_users.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='obtain_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    
]

# Servir les fichiers médias en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
