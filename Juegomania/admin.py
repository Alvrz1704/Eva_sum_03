from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Categoria, Juego, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'get_precio_formateado', 'stock', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

    def get_precio_formateado(self, obj):
        return f"${obj.precio:,.0f}".replace(",", ".")
    get_precio_formateado.short_description = "Precio"

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'juego', 'nombre_cliente', 'cantidad', 'fecha_pedido')
    list_filter = ('juego',)
    search_fields = ('nombre_cliente', 'correo', 'codigo')