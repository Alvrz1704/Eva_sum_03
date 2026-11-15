from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Categoria, Pedido

def catalogo_view(request):
    """Muestra el catálogo de juegos con opciones de búsqueda y filtrado por categoría."""
    query = request.GET.get('q', '')
    cat_id = request.GET.get('categoria', '')
    
    juegos = Juego.objects.all()
    
    if query:
        juegos = juegos.filter(nombre__icontains=query)
    if cat_id:
        juegos = juegos.filter(categoria_id=cat_id)
        
    categorias = Categoria.objects.all()
    
    context = {
        'juegos': juegos,
        'categorias': categorias,
        'q': query,
        'cat_id': cat_id,
    }
    return render(request, 'Juegomania/catalogo.html', context)

def detalle_juego_view(request, juego_id):
    """Muestra el detalle de un juego específico y procesa el formulario de compra con validación de stock."""
    juego = get_object_or_404(Juego, id=juego_id)
    error_mensaje = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        cantidad = int(request.POST.get('cantidad', 1))

        # Validaciones de stock y límites por compra
        if cantidad > 5:
            error_mensaje = "No puedes pedir más de 5 unidades por compra."
        elif cantidad > juego.stock:
            error_mensaje = f"Stock insuficiente. Solo quedan {juego.stock} unidades disponibles."
        else:
            # Descontar stock y actualizar disponibilidad si llega a 0
            juego.stock -= cantidad
            if juego.stock == 0:
                juego.disponible = False
            juego.save()

            # Crear el registro del pedido en la base de datos
            pedido = Pedido.objects.create(
                juego=juego,
                nombre_cliente=nombre,
                correo=correo,
                telefono=telefono,
                cantidad=cantidad
            )

            # Guardar el ID en la sesión y redirigir al comprobante
            request.session['ultimo_pedido_id'] = pedido.id
            return redirect('comprobante')

    context = {
        'juego': juego,
        'error_mensaje': error_mensaje,
    }
    return render(request, 'Juegomania/detalle_juego.html', context)

def comprobante_view(request):
    """Genera y muestra el comprobante del último pedido realizado utilizando la sesión."""
    pedido_id = request.session.get('ultimo_pedido_id')
    
    # Si no hay un pedido activo en la sesión, redirige al catálogo por seguridad
    if not pedido_id:
        return redirect('catalogo')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    total = pedido.juego.precio * pedido.cantidad
    total_clp = f"${total:,.0f} CLP".replace(',', '.')

    context = {
        'pedido': pedido,
        'total_clp': total_clp,
    }
    return render(request, 'Juegomania/comprobante.html', context)