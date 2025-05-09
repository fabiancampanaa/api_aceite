from .models import Busqueda, CustomUser, BusquedaRrss
from .serializers import BusquedaSerializer, CustomUserSerializer, BusquedaRrssSerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.utils.dateparse import parse_date
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
import pandas as pd
from django.db import transaction
import logging
# Create your views here.

class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer

class BusquedaRrssViewSet(viewsets.ModelViewSet):
    queryset = BusquedaRrss.objects.all()
    serializer_class = BusquedaRrssSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


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
@permission_classes([AllowAny])
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



class CargarExcelBusquedaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        excel_file = request.FILES.get('archivo1')

        if not excel_file:
            return Response({'error': 'No se recibió ningún archivo'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(excel_file)
        except Exception as e:
            return Response({'error': f'Error al leer el archivo Excel: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        Busqueda.objects.all().delete()
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
                    id_registro = row.get('id_registro'),
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



logger = logging.getLogger(__name__)



class CargarExcelBusquedaRRSSView(APIView):
    permission_classes = [IsAuthenticated]

    REQUIRED_COLUMNS = [
        'rrss', 'marca', 'nombre_usuario', 'url_instagram', 'seguidores',
        'cant_publicaciones', 'orden', 'publicacion', 'tipo', 'cant_me_gusta',
        'cant_comentarios', 'fecha_subido', 'fecha_ultima', 'valoracion',
        'fecha_registro', 'url'
    ]

    def post(self, request):
        # Validate file presence
        if 'archivo2' not in request.FILES:
            logger.error('No se recibió ningún archivo en la solicitud')
            return Response(
                {'error': 'Debe proporcionar un archivo Excel bajo la clave "archivo2"'},
                status=status.HTTP_400_BAD_REQUEST
            )

        excel_file = request.FILES['archivo2']

        

        # Validate file type
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            logger.error(f'Archivo con extensión no permitida: {excel_file.name}')
            return Response(
                {'error': 'El archivo debe ser un documento Excel (.xlsx o .xls)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Read Excel with specific dtype for certain columns to prevent type issues
            df = pd.read_excel(
                excel_file,
                dtype={
                    'rrss': str,
                    'marca': str,
                    'nombre_usuario': str,
                    'url_instagram': str,
                    'publicacion': str,
                    'tipo': str,
                    'url': str
                },
                parse_dates=[
                    'fecha_subido',
                    'fecha_ultima',
                    'fecha_registro'
                ]
            )
        except Exception as e:
            logger.exception('Error al leer el archivo Excel')
            return Response(
                {'error': f'El archivo Excel está corrupto o no es válido: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate required columns
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            logger.error(f'Columnas faltantes en el archivo Excel: {missing_cols}')
            return Response(
                {'error': f'Faltan columnas requeridas: {missing_cols}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        BusquedaRrss.objects.all().delete()
        registros_creados = 0
        errores = []

        with transaction.atomic():
            for index, row in df.iterrows():
                row_num = index + 2  # Excel rows start at 1 + header row
                
                try:
                    # Manejo especial para campos de fecha
                    fecha_subido = row['fecha_subido'] if not pd.isna(row['fecha_subido']) else None
                    fecha_ultima = row['fecha_ultima'] if not pd.isna(row['fecha_ultima']) else None
                    fecha_registro = row['fecha_registro'] if not pd.isna(row['fecha_registro']) else None
                    if fecha_subido is None:  # Ajusta según tus requisitos
                        raise ValueError("El campo 'fecha_subido' es requerido y no puede estar vacío")
                    # Validate required fields are not empty
                    required_fields = {
                        'rrss': row['rrss'],
                        'marca': row['marca'],
                        'nombre_usuario': row['nombre_usuario'],
                        'url_instagram': row['url_instagram'],
                        'publicacion': row['publicacion'],
                        'tipo': row['tipo'],
                        'url': row['url']
                    }

                    for field, value in required_fields.items():
                        if pd.isna(value) or value == '':
                            raise ValueError(f"El campo '{field}' no puede estar vacío")

                    # Convert numeric fields properly
                    numeric_fields = {
                        'seguidores': row['seguidores'],
                        'cant_publicaciones': row['cant_publicaciones'],
                        'orden': row['orden'],
                        'cant_me_gusta': row['cant_me_gusta'],
                        'cant_comentarios': row['cant_comentarios'],
                        'valoracion': row['valoracion']
                    }

                    for field, value in numeric_fields.items():
                        if pd.isna(value):
                            numeric_fields[field] = None

                    # Create the record
                    BusquedaRrss.objects.create(
                        rrss=required_fields['rrss'],
                        marca=required_fields['marca'],
                        nombre_usuario=required_fields['nombre_usuario'],
                        url_instagram=required_fields['url_instagram'],
                        seguidores=numeric_fields['seguidores'],
                        cant_publicaciones=numeric_fields['cant_publicaciones'],
                        orden=numeric_fields['orden'],
                        publicacion=required_fields['publicacion'],
                        tipo=required_fields['tipo'],
                        cant_me_gusta=numeric_fields['cant_me_gusta'],
                        cant_comentarios=numeric_fields['cant_comentarios'],
                        fecha_subido=fecha_subido,
                        fecha_ultima=fecha_ultima,
                        valoracion=numeric_fields['valoracion'],
                        fecha_registro=fecha_registro,
                        url=required_fields['url'],
                    )
                    registros_creados += 1

                except Exception as e:
                    error_msg = f"Fila {row_num}: {str(e)}"
                    errores.append(error_msg)
                    logger.error(error_msg)
                    continue  # Continue with next row even if this one fails

        response_data = {
            'registros_creados': registros_creados,
            'registros_fallidos': len(errores),
            'total_registros': len(df),
            'errores': errores
        }

        if errores:
            logger.warning(
                f'Proceso completado con errores. '
                f'Creados: {registros_creados}, Fallidos: {len(errores)}'
            )
            response_data['advertencia'] = 'Algunos registros no se pudieron procesar'
            return Response(response_data, status=status.HTTP_207_MULTI_STATUS)

        logger.info(f'Se crearon exitosamente {registros_creados} registros')
        return Response(response_data, status=status.HTTP_201_CREATED)