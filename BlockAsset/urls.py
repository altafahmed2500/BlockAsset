"""
URL configuration for BlockAsset project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('api/user/', include('UserAdmin.urls')),
                  path("api/file/", include("FileAdmin.urls")),
                  path("api/web3/", include("Web3Backend.urls")),
                  path("api/account/", include("AccountAdmin.urls")),
                  path("api/assets/", include("AssetAdmin.urls")),
                  path("api/wearable-data", include("AIAdmin.urls")),
                  path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
