from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_view, name='catalogo'),
    path('juego/<int:juego_id>/', views.detalle_juego_view, name='detalle_juego'),
    path('comprobante/', views.comprobante_view, name='comprobante'),
]