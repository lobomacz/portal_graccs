from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.db import transaction
from django.urls import reverse_lazy
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_gis import filters
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from sispro.permissions import IsOwnerOrReadOnly
from sispro.serializers import *
from sispro.models import *
from suir.models import Comunidad, DetalleTabla
import datetime
import json


# Create your views here.

# Mixins

# Mixin de digitador
class DigitadorMixin():
	def perform_create(self, serializer):
		serializer.save(digitador=self.request.user)


# Vistas principales

# Vista de ingreso de usuarios(login)
class LoginView(ObtainAuthToken):

	permission_classes = [permissions.AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'token': token.key,
			'id': user.pk,
			'username': user.username,
			'first_name': user.first_name,
			'last_name': user.last_name,
			'email': user.email,
			'is_superuser': user.is_superuser,
			'is_active': user.is_active
			})


# ViewSet de gestión de datos de usuario
class MeViewSet(generics.UpdateAPIView, viewsets.GenericViewSet):

	queryset = User.objects.all()
	serializer_class = UserSerializer

	def partial_update(self, request, pk=None):
		user = self.get_object()
		serializer = self.get_serializer(user, data=request.data, partial=True)
		if serializer.is_valid():
			try:
				user = serializer.save()
			except Exception as err:
				return Response({'message': err}, status=status.HTTP_400_BAD_REQUEST)
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		else:
			return Response({'message': '¡Error de validación de datos!'}, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False)
	def refresh(self, request):
		user = request.user
		serializer = self.get_serializer(user, many=False) # UserSerializer(user, many=False)
		return Response(serializer.data)

	@action(detail=False, methods=['post'])
	def check_password(self, request):
		user = request.user
		password = request.data.get('password')
		authenticated = authenticate(request, username=user.username, password=password)
		if authenticated is not None:
			return Response({'message': '¡Contraseña validada!'})
		else:
			return Response({'message': '¡Contraseña no-validada!'}, status=status.HTTP_400_BAD_REQUEST)

	@action(detail=False, methods=['post'])
	def change_password(self, request):
		user = request.user
		password = request.data.get('password')
		authenticated = authenticate(request, username=user.username, password=password)

		if authenticated == None:
			return Response({'message': 'La acción no es permitida sin la validación de la contraseña.'}, status=status.HTTP_403_FORBIDDEN)
		else:
			new_password = request.data.get('newPassword')
			user.set_password(new_password)
			user.save()
			return Response({'message': 'La contraseña se modificó con éxito.'}, status=status.HTTP_202_ACCEPTED)



# Vista para comprobación de permisos
class PermissionView(APIView):
	
	def get(self, request, format=None):
		user = request.user
		perm = request.query_params.get('perm')
		has_perm = user.has_perm('sispro.' + perm)
		return Response({ perm: has_perm })


# VieSet DetalleTabla
class DetalleTablaViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	Viewset de tablas de uso general
	"""
	queryset = DetalleTabla.objects.all()
	serializer_class = sDetalleTabla
	permission_classes = [permissions.AllowAny]
	pagination_class = None
	page_size = None

	@action(detail=False)
	def articulos(self, request):
		articulos = self.get_queryset().filter(tabla__tabla='articulos')
		serializer = self.get_serializer(articulos, many=True)
		return Response(serializer.data)

	@action(detail=False)
	def unidades(self, request):
		unidades = self.get_queryset().filter(tabla__tabla='unidades')
		serializer = self.get_serializer(unidades, many=True)
		return Response(serializer.data)


# ViewSet de Programas
class ProgramasViewSet(viewsets.ReadOnlyModelViewSet):

	queryset = Programa.objects.all()
	serializer_class = sPrograma
	filter_backends = [SearchFilter]
	search_fields = ['nombre','codigo']
	permission_classes = [permissions.AllowAny]


# ViewSet de Proyectos para lista de combos
class ListaProyectosView(generics.ListAPIView):
	queryset = Proyecto.objects.filter(finalizado=False)
	serializer_class = sProyecto
	pagination_class = None
	page_size = None


# ViewSet de Proyectos
class ProyectosViewSet(viewsets.ReadOnlyModelViewSet):

	queryset = Proyecto.objects.all()
	serializer_class = sProyecto
	filter_backends = [SearchFilter]
	search_fields = ['nombre', 'codigo']
	permission_classes = [permissions.AllowAny]

	@action(detail=False)
	def activos(self, request):
		proyectos = Proyecto.objects.filter(finalizado=False)
		serializer = self.get_serializer(proyectos, many=True)
		return Response(serializer.data)


# ViewSet de Tecnicos
class TecnicosViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	Un viewset sencillo para visualizar técnicos
	"""
	queryset = Tecnico.objects.all()
	serializer_class = sTecnico
	pagination_class = None
	page_size = None

	@action(detail=False)
	def activos(self, request):
		tecnicos = self.get_queryset().filter(activo=True)
		serializer = self.get_serializer(tecnicos, many=True)
		return Response(serializer.data)


# ViewSet de Comunidades
class ComunidadesViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	Un viewset sencillo para visualizar técnicos
	"""
	queryset = Comunidad.objects.all()
	serializer_class = sComunidad
	pagination_class = None
	page_size = None


# ViewSet de Etnias
class EtniasViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	Un viewset sencillo para visualizar datos de etnias
	"""
	queryset = DetalleTabla.objects.filter(tabla__tabla='etnias')
	serializer_class = sDetalleTabla


# ViewSet de Bonos
class BonosViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	Viewset para recuperar datos de Bonos
	"""
	queryset = Bono.objects.filter(tipo__elemento='bono')
	serializer_class = sBono
	pagination_class = None
	page_size = None


# ViewSet de Planes de Inversión
class PlanesViewSet(BonosViewSet):
	"""
	Hereda de BonosViewSet y únicamente utiliza un queryset distinto
	"""
	queryset = Bono.objects.filter(tipo__elemento='plan de inversion')


# Vieset de Protagonistas para listas de combos
class ListaProtagonistasView(generics.ListAPIView):
	queryset = Protagonista.objects.all()
	serializer_class = sProtagonista
	pagination_class = None
	page_size = None



# ViewSet de Protagonistas
class ProtagonistasViewSet(viewsets.ModelViewSet):

	queryset = Protagonista.objects.all()
	serializer_class = sProtagonista
	filterset_fields = ['cedula']



# ViewSet de Bonos entregados
class ProtagonistasBonosViewSet(viewsets.ModelViewSet):

	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='bono')
	filterset_fields = ['bono__nombre']
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
	serializer_class = sProtagonistaBono
	srid = 4326


	def initial(self, request, *args, **kwargs):
		super().initial(request, *args, **kwargs)
		if 'location' in request.data.keys() and request.data['location'] != None:
			if 'srid' in request.data['location'].keys():
				self.srid = request.data['location']['srid']


	def perform_create(self, serializer):
		point = serializer.validated_data.get('location')

		if self.srid != 4326 and point != None:
			point = Point(point.coords[0], point.coords[1], srid=self.srid)
			point.transform(4326)

		serializer.save(location=point, digitador=self.request.user)


	def perform_update(self, serializer):
		point = serializer.validated_data.get('location')

		if self.srid != 4326 and point != None:
			point = Point(point.coords[0], point.coords[1], srid=self.srid)
			point.transform(4326)

		serializer.save(location=point, actualizado_por=self.request.user)


	@action(detail=False)
	def lista(self, request):
		bonos = self.get_queryset().filter(activo=True)
		serializer = sProtagonistaBono2(bonos, many=True)
		return Response(serializer.data)


	@action(detail=True)
	def entregados(self, request, pk=None):
		bonos = self.get_queryset().filter(protagonista__cedula=pk)
		serializer = sProtagonistaBono2(bonos, many=True)
		return Response(serializer.data)




# ViewSet de Planes de Inversión entregados
class ProtagonistasPlanesViewSet(ProtagonistasBonosViewSet):
	"""
	Hereda de ProtagonistasBonosViewSet usuando solamente un queryset que filta
	los bonos de tipo 'plan de inversion'
	"""
	queryset = ProtagonistaBono.objects.filter(bono__tipo__elemento='plan de inversion')


	

# ViewSet de Capitalizaciones de Planes de Inversión
class CapitalizacionViewSet(viewsets.ModelViewSet):

	queryset = Capitalizacion.objects.all()
	serializer_class = sCapitalizacion
	permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
	filterset_fields = ['p_bono__protagonista__cedula']

	@action(detail=False)
	def por_plan(self, request):
		
		plan = request.query_params.get('plan')
		edit = request.query_params.get('edit')

		if edit == None:
			self.serializer_class = sCapitalizacionText

		capitalizacion = Capitalizacion.objects.all().filter(p_bono=plan)
		serializer = self.get_serializer(capitalizacion, many=True)
		
		return Response(serializer.data)

	def perform_create(self, serializer):
		serializer.save(digitador=self.request.user)

	def perform_update(self, serializer):
		serializer.save(actualizado_por=self.request.user)



# ViewSet de Aporte a Planes de inversión.
class AporteViewSet(CapitalizacionViewSet):

	queryset = Aporte.objects.filter(p_bono__bono__tipo__elemento='plan de inversion')
	serializer_class = sAporte
	filterset_fields = ['p_bono__protagonista__cedula']



# ViewSet de Capacitaciones
class CapacitacionViewSet(CapitalizacionViewSet):

	queryset = Capacitacion.objects.all()
	serializer_class = sCapacitacion
	filterset_fields = ['protagonista__cedula']





