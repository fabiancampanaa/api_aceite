from .models import Busqueda, CustomUser
from django.contrib.auth.models import User
from rest_framework import serializers

class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields =  ['id_registro', 'id_producto', 'producto', 'marca', 'cantidad', 'unidad_medida', 'envase', 'valor', 'identificacion_url', 'url', 'fecha_extraccion', 'pagina_general']
                   
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'numero_telefono', 'nombre_empresa', 'tipo']