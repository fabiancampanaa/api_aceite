from .models import Busqueda, CustomUser
from .serializers import BusquedaSerializer, CustomUserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    user = get_object_or_404(CustomUser, email=request.data['email'])
    print(request.data['password'])
    if not user.check_password(request.data['password']):
        return Response({"error":"Contraseña incorrecta"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer = CustomUserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    print(request.data)
    serializer  = CustomUserSerializer(data=request.data)
    print(serializer)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()

        user = CustomUser.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token' : token.key, 'user' : serializer.data}, status=status.HTTP_201_CREATED)
    
    return  Response(serializer.errors, status=status.HTTP_409_CONFLICT)          
   

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def profile(request):
    print(request.data)
    return Response({})
   