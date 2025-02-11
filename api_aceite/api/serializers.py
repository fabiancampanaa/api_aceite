from .models import Busqueda
from django.contrib.auth.models import User
from rest_framework import serializers

class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']