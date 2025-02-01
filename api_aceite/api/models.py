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

