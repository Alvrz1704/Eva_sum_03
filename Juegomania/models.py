from django.db import models
import uuid
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Juego")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    imagen = models.ImageField(upload_to='juegos/', verbose_name="Imagen de la Caja")
    precio = models.PositiveIntegerField(verbose_name="Precio (CLP)")
    jugadores = models.CharField(max_length=50, verbose_name="Cantidad de Jugadores")
    edad_minima = models.PositiveIntegerField(verbose_name="Edad Mínima")
    stock = models.PositiveIntegerField(verbose_name="Stock en Bodega")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para la venta")

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    codigo = models.CharField(max_length=36, unique=True, editable=False, verbose_name="Código de Pedido")
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, verbose_name="Juego")
    nombre_cliente = models.CharField(max_length=150, verbose_name="Nombre de quien pide")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad de Unidades")
    fecha_pedido = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.codigo} - {self.nombre_cliente}"