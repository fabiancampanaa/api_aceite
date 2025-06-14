from .models import Busqueda, CustomUser, BusquedaRrss
from django.contrib.auth.models import User
from rest_framework import serializers

class BusquedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Busqueda
        fields =  ['id_registro', 'id_producto', 'producto', 'marca', 'cantidad', 'unidad_medida', 'envase', 'valor', 'identificacion_url', 'url', 'fecha_extraccion', 'pagina_general', 'precio_litro']
                   
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password', 'numero_telefono', 'tipo_usuario', 'tipo_acceso']
        

class BusquedaRrssSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusquedaRrss
        fields =  ['rrss', 'marca', 'nombre_usuario', 'url_instagram', 'seguidores', 'cant_publicaciones', 'orden', 'publicacion', 'tipo', 'cant_me_gusta', 'cant_comentarios', 'fecha_subido', 'fecha_ultima', 'valoracion', 'fecha_registro', 'url']