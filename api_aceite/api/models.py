from django.contrib.auth.models import AbstractUser
from django.db import models

class Busqueda(models.Model):
    id_registro = models.IntegerField()
    id_producto = models.IntegerField()
    producto = models.CharField(max_length=150)
    marca = models.CharField(max_length=150)
    cantidad = models.IntegerField()
    unidad_medida = models.CharField(max_length=10)
    envase = models.CharField(max_length=150)
    valor = models.IntegerField()
    identificacion_url = models.CharField(max_length=500)
    url = models.URLField()
    fecha_extraccion = models.DateField()
    pagina_general = models.URLField()


class CustomUser(AbstractUser):
    numero_telefono = models.CharField(max_length=9, blank=True, null=True)
    tipo = models.CharField(max_length=20, default="basico")
    nombre_empresa = models.CharField(max_length=50, blank=True, null=True)

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

