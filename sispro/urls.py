from django.urls import include, path
from rest_framework.routers import DefaultRouter
from sispro.views import *


# Creamos un router para la API

router = DefaultRouter()
router.register(r'tablas', DetalleTablaViewSet)
router.register(r'programas', ProgramasViewSet)
router.register(r'proyectos', ProyectosViewSet)
router.register(r'tecnicos', TecnicosViewSet)
router.register(r'comunidades', ComunidadesViewSet)
router.register(r'etnias', EtniasViewSet)
router.register(r'protagonistas', ProtagonistasViewSet)
router.register(r'bonos', BonosViewSet)
router.register(r'planes', PlanesViewSet)
router.register(r'bonos-protagonista', ProtagonistasBonosViewSet)
router.register(r'planes-protagonista', ProtagonistasPlanesViewSet)
router.register(r'capitalizacion', CapitalizacionViewSet)
router.register(r'aportes', AporteViewSet)
router.register(r'capacitacion', CapacitacionViewSet)
router.register(r'me', MeViewSet)

urlpatterns = [
	path('auth/', LoginView.as_view(), name='sispro_login'),
	path('has-perm/', PermissionView.as_view(), name='sispro_permission'),
	path('lista-protagonistas/', ListaProtagonistasView.as_view(), name='sispro_all_protagonistas'),
	path('lista-proyectos/', ListaProyectosView.as_view(), name='sispro_all_proyectos'),
	path('', include(router.urls)),
]
