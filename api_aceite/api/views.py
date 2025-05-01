from .models import Busqueda, CustomUser, BusquedaRrss
from .serializers import BusquedaSerializer, CustomUserSerializer, BusquedaRrssSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from django.views import View
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from .models import Busqueda
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer

class BusquedaRrssViewSet(viewsets.ModelViewSet):
    queryset = BusquedaRrss.objects.all()
    serializer_class = BusquedaRrssSerializer



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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import datetime
import pandas as pd
from .models import Busqueda

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.dateparse import parse_date
from datetime import datetime
import pandas as pd
from .models import Busqueda

class CargarExcelBusquedaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        excel_file = request.FILES.get('archivo')

        if not excel_file:
            return Response({'error': 'No se recibió ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({'error': f'Error al leer el archivo Excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        registros_creados = 0
        errores = []

        for index, row in df.iterrows():
            try:
                # Limpieza
                cantidad = float(str(row.get('cantidad')).replace('–', '-').replace('“', '').replace('”', ''))
                valor = float(str(row.get('valor')).replace('–', '-').replace('“', '').replace('”', ''))
                unidad = str(row.get('unidad_medida')).lower()

                # Conversión a litros
                if unidad == 'ml':
                    cantidad_litros = cantidad / 1000
                elif unidad == 'l':
                    cantidad_litros = cantidad
                else:
                    raise ValueError("Unidad de medida inválida")

                if cantidad_litros <= 0:
                    raise ValueError("Cantidad en litros no válida")

                precio_litro = valor / cantidad_litros

                # Parsear y validar fecha
                fecha_raw = row.get('fecha_extraccion')
                fecha_extraccion = None

                if isinstance(fecha_raw, str):
                    fecha_extraccion = parse_date(fecha_raw)
                elif isinstance(fecha_raw, (int, float)):
                    fecha_extraccion = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(fecha_raw) - 2).date()

                if not fecha_extraccion:
                    raise ValueError("Fecha de extracción inválida")

                # Crear el objeto
                Busqueda.objects.create(
                    id_producto=row.get('id_producto'),
                    producto=row.get('producto'),
                    marca=row.get('marca'),
                    cantidad=cantidad,
                    unidad_medida=row.get('unidad_medida'),
                    envase=row.get('envase'),
                    valor=valor,
                    precio_litro=precio_litro,
                    identificacion_url=row.get('identificacion_url'),
                    url=row.get('url'),
                    fecha_extraccion=fecha_extraccion,
                    pagina_general=row.get('pagina_general'),
                )

                registros_creados += 1

            except Exception as e:
                errores.append(f"Fila {index + 2}: {str(e)}")

        return Response({
            'mensaje': f'{registros_creados} registros creados exitosamente',
            'errores': errores
        }, status=status.HTTP_200_OK)
