from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.dateparse import parse_date
from datetime import datetime

class Busqueda(models.Model):
    id_producto = models.IntegerField()
    producto = models.CharField(max_length=150)
    marca = models.CharField(max_length=150)
    cantidad = models.IntegerField()  # Puede estar en ml o L
    unidad_medida = models.CharField(max_length=10)  # "ml" o "L"
    envase = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=12, decimal_places=2)  # Precio total
    precio_litro = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # Precio homologado
    identificacion_url = models.CharField(max_length=500)
    url = models.URLField()
    fecha_extraccion = models.DateField()
    pagina_general = models.URLField()








class CustomUser(AbstractUser):
    numero_telefono = models.CharField(max_length=9, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, default="basico")
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",  # ← Evita el conflicto con User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_users_permissions",  # ← Evita el conflicto con User.user_permissions
        blank=True
    )

    def __str__(self):
        return self.username

class BusquedaRrss(models.Model):
    rrss = models.CharField(max_length=150)
    marca = models.CharField(max_length=150)
    nombre_usuario = models.CharField(max_length=150)
    url_instagram = models.CharField(max_length=150)
    seguidores = models.IntegerField()
    cant_publicaciones = models.IntegerField()
    orden = models.IntegerField()
    publicacion = models.TextField()
    tipo = models.CharField(max_length=150)
    cant_me_gusta = models.IntegerField()
    cant_comentarios = models.IntegerField()
    fecha_subido = models.CharField(max_length=200)
    fecha_ultima = models.DateField()
    valoracion = models.CharField(max_length=150)
    fecha_registro = models.DateField()
    url = models.URLField()