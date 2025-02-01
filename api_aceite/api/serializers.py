from .models import Busqueda
from rest_framework import serializers

class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields = '__all__'