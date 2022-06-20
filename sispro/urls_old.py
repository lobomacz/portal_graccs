from django.urls import include, path
from sispro.views import *

urlpatterns = [
	path('', InicioView.as_view(), name='inicio_sispro'),
	path('login/', LoginView.as_view(), name='login_sispro'),
	path('logout/', LogoutView.as_view(), name='logout_sispro'),
	path('programas/', ListaProgramasView.as_view(), name='lista_programas'),
	path('programas/buscar/',ListaFiltroProgramasView.as_view(), name='lista_filtro_programas'),
	path('programas/<int:pk>/', DetalleProgramaView.as_view(), name='detalle_programa'),
	path('proyectos/', ListaProyectosView.as_view(), name='lista_proyectos'),
	path('proyectos/buscar/', ListaFiltroProyectosView.as_view(), name='lista_filtro_proyectos'),
	path('proyectos/<int:pk>/', DetalleProyectoView.as_view(), name='detalle_proyecto'),
	path('protagonistas/', include([
		path('', ListaProtagonistasView.as_view(), name='lista_protagonistas'),
		path('menu/', MenuProtagonistasView.as_view(), name='menu_protagonistas'),
		path('buscar/', ListaFiltroProtagonistasView.as_view(), name='lista_filtro_protagonistas'),
		path('nuevo/', CreateProtagonistaView.as_view(), name='nuevo_protagonista'),
		path('<str:pk>/', DetalleProtagonistaView.as_view(), name='detalle_protagonista'),
		path('<str:pk>/editar/', UpdateProtagonistaView.as_view(), name='update_protagonista'),
		])),
	path('bonos/', include([
		path('', ListaBonosView.as_view(), name='lista_bonos'),
		path('buscar/', ListaFiltroBonosView.as_view(), name='lista_filtro_bonos'),
		path('nuevo/', CreateBonoView.as_view(), name='nuevo_bono'),
		path('<int:pk>/', DetalleBonoView.as_view(), name='detalle_bono'),
		path('<int:pk>/editar/', UpdateBonoView.as_view(), name='update_bono'),
		])),
	path('planes-inversion/', include([
		path('', ListaPlanesInversionView.as_view(), name='lista_planes_inversion'),
		path('buscar/', ListaFiltroPlanesInversionView.as_view(), name='lista_filtro_planes_inversion'),
		path('nuevo/', CreatePlanInversionView.as_view(), name='nuevo_plan_inversion'),
		path('<int:pk>/', DetallePlanInversionView.as_view(), name='detalle_plan_inversion'),
		path('<int:pk>/editar/', UpdatePlanInversionView.as_view(), name='update_plan_inversion'),
		])),
]


