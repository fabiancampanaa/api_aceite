from django.shortcuts import render
from .models import Busqueda
from .serializers import BusquedaSerializer
from rest_framework import viewsets
# Create your views here.

class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer