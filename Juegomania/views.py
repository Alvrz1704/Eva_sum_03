from django.shortcuts import render, get_object_or_404, redirect
from .models import Juego, Categoria, Pedido

def formatear_clp(valor):
    """Formatea un número entero a pesos chilenos (ej: $45.000 CLP)."""
    return f"${valor:,.0f} CLP".replace(',', '.')

def catalogo_view(request):
    """Muestra el catálogo principal en (/) solo con juegos disponibles, busqueda y categorias."""
    query = request.GET.get('q', '').strip()
    cat_id = request.GET.get('categoria', '').strip()
    
    # REGLA ESTRICTA: Solo trae juegos cuya casilla 'disponible' esté marcada como True en el admin.
    # Si un juego como 'Clue' se desmarca, se excluye automáticamente de aquí.
    juegos = Juego.objects.filter(disponible=True)
    
    if query:
        juegos = juegos.filter(nombre__icontains=query)
    if cat_id:
        juegos = juegos.filter(categoria_id=cat_id)
        
    # Asignamos el precio formateado en CLP a cada juego
    for juego in juegos:
        juego.precio_clp = formatear_clp(juego.precio)
        
    categorias = Categoria.objects.all()
    
    context = {
        'juegos': juegos,
        'categorias': categorias,
        'q': query,
        'cat_id': cat_id,
    }
    return render(request, 'Juegomania/catalogo.html', context)

def detalle_juego_view(request, juego_id):
    """Muestra el detalle solo si está disponible, de lo contrario lanza 404."""
    juego = get_object_or_404(Juego, id=juego_id, disponible=True)
    juego.precio_clp = formatear_clp(juego.precio)
    error_mensaje = None

    if request.method == 'POST':
        if juego.stock <= 0:
            error_mensaje = "Este juego está agotado y no permite realizar pedidos."
        else:
            nombre = request.POST.get('nombre')
            correo = request.POST.get('correo')
            telefono = request.POST.get('telefono')
            cantidad = int(request.POST.get('cantidad', 1))

            if cantidad < 1:
                error_mensaje = "La cantidad debe ser al menos 1."
            elif cantidad > 5:
                error_mensaje = "No puedes pedir más de 5 unidades por compra."
            elif cantidad > juego.stock:
                error_mensaje = f"Stock insuficiente. Solo quedan {juego.stock} unidades disponibles."
            else:
                juego.stock -= cantidad
                juego.save()

                pedido = Pedido.objects.create(
                    juego=juego,
                    nombre_cliente=nombre,
                    correo=correo,
                    telefono=telefono,
                    cantidad=cantidad
                )

                request.session['ultimo_pedido_id'] = pedido.id
                return redirect('comprobante')

    context = {
        'juego': juego,
        'error_mensaje': error_mensaje,
    }
    return render(request, 'Juegomania/detalle_juego.html', context)

def comprobante_view(request):
    pedido_id = request.session.get('ultimo_pedido_id')
    if not pedido_id:
        return redirect('catalogo')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    total = pedido.juego.precio * pedido.cantidad
    total_clp = formatear_clp(total)

    context = {
        'pedido': pedido,
        'total_clp': total_clp,
    }
    return render(request, 'Juegomania/comprobante.html', context)