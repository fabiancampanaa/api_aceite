from .models import Busqueda, CustomUser
from django.contrib.auth.models import User
from rest_framework import serializers

class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'numero_telefono', 'nombre_empresa', 'tipo']