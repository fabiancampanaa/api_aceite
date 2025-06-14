"""
URL configuration for api_aceite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path

from api import views

from rest_framework import routers

router = routers.DefaultRouter()

# En el router vamos añadiendo los endpoints a los viewsets
router.register('busquedas', views.BusquedaViewSet)
router.register('busquedasrrss', views.BusquedaRrssViewSet)
router.register('users', views.UsuarioViewSet)


urlpatterns = [
  path('api/v1/', include(router.urls)),
  path('admin/', admin.site.urls),
  
  path('api/archivo1/', views.CargarExcelBusquedaView.as_view(), name='cargar_excel_busqueda'),
   path('api/archivo2/', views.CargarExcelBusquedaRRSSView.as_view(), name='cargar_excel_rrss'),
  re_path('login', views.login),
  re_path('api/register', views.register)
]