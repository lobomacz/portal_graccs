from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from suir.models import DetalleTabla, Comunidad
from sispro.models import *

# Serializadores de modelos


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		exclude = ['password', 'last_login', 'date_joined', 'is_staff', 'groups', 'user_permissions']


class sTecnico(serializers.ModelSerializer):

	class Meta:
		model = Tecnico
		fields = ['cedula', 'nombres', 'apellidos']


class sPrograma(serializers.ModelSerializer):

	class Meta:
		model = Programa
		fields = '__all__'



class sProyecto(serializers.ModelSerializer):

	sector = serializers.StringRelatedField(many=False)

	class Meta:
		model = Proyecto
		fields = ['id', 'codigo', 'nombre', 'acronimo', 'sector']


class sBono(serializers.ModelSerializer):

	tipo = serializers.StringRelatedField(many=False)

	class Meta:
		model = Bono
		fields = '__all__'


class sComunidad(serializers.ModelSerializer):

	municipio = serializers.StringRelatedField(many=False)

	class Meta:
		model = Comunidad
		fields = '__all__'


class sDetalleTabla(serializers.ModelSerializer):

	class Meta:
		model = DetalleTabla
		fields = '__all__'


class sProtagonistaBono(GeoFeatureModelSerializer):

	protagonista = serializers.PrimaryKeyRelatedField(queryset=Protagonista.objects.all())
	bono = serializers.PrimaryKeyRelatedField(queryset=Bono.objects.all())
	proyecto = serializers.PrimaryKeyRelatedField(queryset=Proyecto.objects.all())
	tecnico = serializers.PrimaryKeyRelatedField(queryset=Tecnico.objects.all(), allow_null=True)
	comunidad = serializers.PrimaryKeyRelatedField(queryset=Comunidad.objects.all())
	digitador = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)

	class Meta:
		model = ProtagonistaBono
		geo_field = 'location'
		fields = '__all__'


class sProtagonistaBono2(serializers.ModelSerializer):

	protagonista = serializers.StringRelatedField(many=False)
	bono = serializers.StringRelatedField(many=False)
	proyecto = serializers.StringRelatedField(many=False)

	class Meta:
		model = ProtagonistaBono
		fields = ['id', 'protagonista', 'bono', 'proyecto', 'fecha_recibido']



class sProtagonista(serializers.ModelSerializer):

	comunidad = serializers.StringRelatedField(many=False)
	etnia = serializers.StringRelatedField(many=False)
	bonos = sProtagonistaBono2(many=True, read_only=True)

	class Meta:
		model = Protagonista
		fields = '__all__'



class sCapitalizacion(serializers.ModelSerializer):

	p_bono = serializers.PrimaryKeyRelatedField(queryset=ProtagonistaBono.objects.all())
	articulo = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.filter(tabla__tabla="articulos"))
	unidad = serializers.PrimaryKeyRelatedField(queryset=DetalleTabla.objects.filter(tabla__tabla="unidades"))
	digitador = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

	class Meta:
		model = Capitalizacion
		fields = '__all__'


class sCapitalizacionText(serializers.ModelSerializer):

	articulo = serializers.StringRelatedField(many=False)
	unidad = serializers.StringRelatedField(many=False)

	class Meta:
		model = Capitalizacion
		fields = ['articulo', 'unidad', 'cantidad', 'costo', 'total']


class sProtagonistaString(serializers.ModelSerializer):

	class Meta:
		model = Protagonista
		fields = ['cedula', 'nombres', 'apellidos']



class sCapacitacion(serializers.ModelSerializer):

	protagonista = serializers.PrimaryKeyRelatedField(queryset=Protagonista.objects.all())
	bono = serializers.PrimaryKeyRelatedField(queryset=Bono.objects.all())
	protagonista_str = sProtagonistaString(many=False, read_only=True)

	class Meta:
		model = Capacitacion
		fields = '__all__'


class sAporte(serializers.ModelSerializer):

	p_bono = serializers.PrimaryKeyRelatedField(queryset=ProtagonistaBono.objects.all())

	class Meta:
		model = Aporte
		fields = '__all__'