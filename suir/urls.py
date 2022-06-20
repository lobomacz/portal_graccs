from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from suir.views import *


#  Rutas definidas para el sitio Suir


urlpatterns = [
	path('', InicioView.as_view(), name='inicio'),
    path('noticias/', include([
        path('', ListaPublicacionesView.as_view(tipo='noticia'), name='lista_noticias'),
        path('buscar/', ListaFiltroPublicacionesView.as_view(tipo='noticia'), name='buscar_noticias'),
        path('<slug:slug>/', DetallePublicacionView.as_view(), name='detalle_noticia'),
        ])),
    path('informes/', include([
        path('', ListaPublicacionesView.as_view(tipo='informe'), name='lista_informes'),
        path('buscar/', ListaFiltroPublicacionesView.as_view(tipo='informe'), name='buscar_informes'),
        path('<slug:slug>/', DetallePublicacionView.as_view(), name='detalle_informe'),
        ])),
    path('indicadores/', include([
        path('', ListaIndicadoresView.as_view(), name='lista_indicadores'),
        path('buscar/', ListaFiltroIndicadoresView.as_view(), name='buscar_indicadores'),
        path('<int:pk>/', DetalleIndicadorView.as_view(), name='detalle_indicador'),
        path('valor/<int:pk>/', DetalleValorView.as_view(), name='detalle_valor_indicador'),
        ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)