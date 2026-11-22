from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    nit = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    observaciones = models.CharField(max_length=255)
    estado = models.CharField(max_length=10)

    class Meta:
        db_table = 'proveedor'


class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.BigIntegerField()
    foto = models.CharField(max_length=100)
    cantidad = models.BigIntegerField()
    descripcion = models.CharField(max_length=150)
    fecha = models.CharField(max_length=10)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    class Meta:
        db_table = 'producto'