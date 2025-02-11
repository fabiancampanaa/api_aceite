from django.contrib.auth.models import User
from .models import Busqueda
from .serializers import BusquedaSerializer, UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token

# Create your views here.

class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    return Response({})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    print(request.data)
    serializer  = UserSerializer(data=request.data)
    print(serializer)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
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
   