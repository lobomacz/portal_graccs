from django.conf import settings
from django.contrib.gis.db import models
from django.db.models import Q 
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.contrib.auth.models import User 
from django.urls import reverse 
from django.dispatch import receiver
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from rest_framework.authtoken.models import Token
from suir.models import Tabla, DetalleTabla, Institucion, Comunidad, Contacto


# Create your models here.


# Función para crear tokens para cada usuario

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#
# 	if created:
# 		Token.objects.create(user=instance)


# Tabla de Contactos
class Tecnico(SoftDeletionModel, TimestampsModel):

	""" 
	Clase para el registro de técnicos de las instituciones 
	"""

	cedula = models.CharField(max_length=14, primary_key=True, help_text='Cédula de identidad sin guiones')
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	comunidad = models.ForeignKey(Comunidad, on_delete=models.RESTRICT, help_text='Comunidad de residencia')
	fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True)
	sexo = models.CharField(max_length=1, choices=[('m', 'Masculino'), ('f', 'Femenino')])
	etnia = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, null=True, limit_choices_to=Q(tabla__tabla='etnias'), related_name='contactos_etnias', related_query_name='contacto_etnia')
	telefono = models.CharField(max_length=9, help_text='8888-8888', null=True, blank=True)
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text='Requerido sólo si el usuario tendrá acceso a digitar o extraer datos.')
	activo = models.BooleanField(default=True)

	class Meta:
		ordering = ['institucion', 'apellidos', 'nombres']

	def __str__(self):
		return "{0} {1}".format(self.nombres.upper(), self.apellidos.upper())



# Tabla de Programas
class Programa(models.Model):

	""" 
	Clase para lista de Programas para el registro y agrupación 
	de proyectos por programa. 
	"""

	codigo = models.CharField('Código', max_length=50)
	nombre = models.CharField(max_length=200)
	acronimo = models.CharField('Acrónimo', max_length=45)
	descripcion = models.TextField('Descripción', max_length=500)
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), null=True, blank=True)
	finalizado = models.BooleanField(default=False)

	class Meta:
		ordering = ['finalizado','sector','nombre']

	def __str__(self):
		return "{0} - {1}".format(self.codigo.upper(), self.acronimo.upper())


# Tabla de Proyectos
class Proyecto(models.Model):

	""" 
	Clase para lista de Proyectos para el registro y agrupación 
	de los bonos y planes de inversión por proyecto. 
	"""

	codigo = models.CharField('Código', max_length=50)
	nombre = models.CharField(max_length=200)
	acronimo = models.CharField('Acrónimo', max_length=45)
	programa = models.ForeignKey(Programa, on_delete=models.SET_NULL, null=True, blank=True)
	descripcion = models.CharField('Descripción', max_length=500, null=True, blank=True, default='')
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'))
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)
	contacto = models.ForeignKey(Contacto, on_delete=models.SET_NULL, null=True, blank=True)
	finalizado = models.BooleanField(default=False)

	def __str__(self):
		return "{0} - {1}".format(self.codigo.upper(), self.acronimo.upper())

	class Meta:
		ordering = ['finalizado', 'sector', 'nombre']


# Tabla de Bonos
class Bono(TimestampsModel):
	""" 
	Clase para la lista de Bonos para el registro de los diferentes 
	bonos productivos o planes de inversión 
	ofrecidos por parte del gobierno. 
	"""

	codigo = models.CharField('Código', max_length=50, null=True, blank=True)
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField('Descripción')
	sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), related_name='bonos_sectores', related_query_name='bono_sector')
	# El campo tipo clasifica si se trata de un bono o un plan de inversión 
	tipo = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='tipos_bono'), related_name='bonos_tipos', related_query_name='bono_tipo')
	digitador = models.ForeignKey(User, on_delete=models.RESTRICT)

	class Meta:
		ordering = ['tipo', 'nombre']

	def __str__(self):
		return self.nombre.upper()


# Tabla de Protagonistas
class Protagonista(SoftDeletionModel, TimestampsModel):
	""" 
	Clase Protagonista para el registro de las personas 
	que reciben Bonos/Planes de inversión de los proyectos. 
	"""

	cedula = models.CharField('Cédula', max_length=14, primary_key=True, help_text='Cédula de identidad sin guiones')
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	fecha_nacimiento = models.DateField('Fecha de nacimiento')
	sexo = models.CharField(max_length=1, choices=[('m', 'Masculino'), ('f', 'Femenino')])
	etnia = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='etnias'))
	comunidad = models.ForeignKey(Comunidad, on_delete=models.PROTECT)
	telefono = models.CharField('Teléfono', max_length=9, help_text='8888-8888', null=True, blank=True)
	promotor = models.BooleanField('Es Promotor', default=False)
	jvc = models.BooleanField('Miembro de JVC', default=False)

	def __str__(self):
		return "{0} {1} >>> {2}".format(self.nombres.upper(), self.apellidos.upper(), self.cedula.upper())

	def get_absolute_url(self):
		return ProtagonistasViewSet().reverse_action('retrieve', args=[self.pk]) # reverse('detalle_protagonista', kwargs={'pk':self.pk})

	class Meta:
		ordering = ['apellidos', 'nombres']
		verbose_name = 'Protagonista'



# Tabla de Protagonistas con Bonos/Planes de inversión
class ProtagonistaBono(TimestampsModel, models.Model):
	""" 
	Clase ProtagonistaBono para registro de los Bonos/Planes de inversión
	entregados a protagonistas.
	""" 

	protagonista = models.ForeignKey(Protagonista, on_delete=models.CASCADE)
	bono = models.ForeignKey(Bono, on_delete=models.PROTECT)
	proyecto = models.ForeignKey(Proyecto, on_delete=models.PROTECT)
	fecha_recibido = models.DateField(help_text='Fecha en que recibió el Bono/Plan de inversión.')
	tecnico = models.ForeignKey(Tecnico, on_delete=models.RESTRICT, help_text='Técnico que realizó la entrega.', null=True)
	comunidad = models.ForeignKey(Comunidad, on_delete=models.PROTECT, help_text='Comunidad donde se ejecuta.')
	observaciones = models.CharField(max_length=500, blank=True, null=True)
	digitador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='protagonista_bono_digitador')
	actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='protagonista_bono_actualizador')
	entregado = models.BooleanField(default=False, help_text='El Bono/Plan de inversión se entregó al protagonista.')
	activo = models.BooleanField(default=True, help_text='Está activo para seguimiento.')

	location = models.PointField(null=True)


	def __str__(self):
		return "{0} {1}>>{2}>>{3}".format(self.protagonista.nombres.upper(), self.protagonista.apellidos.upper(), self.bono.codigo.upper(), self.fecha_recibido)


	def get_absolute_url(self):
		return ProtagonistasBonosViewSet().reverse_action('retrieve', args=[self.pk]) # reverse('detalle_protagonista_bono', kwargs={'pk':self.pk})


	class Meta:
		ordering = ['protagonista','-fecha_recibido','bono']
		verbose_name = 'Protagonista con Bono/Plan'
		verbose_name_plural = 'Protagonistas con Bonos/Planes'


# Tabla de Capitalizacion
class Capitalizacion(TimestampsModel):
	"""
	Clase CapitalizacionBono para registrar la capitalización de los Bonos/Planes de inversión
	entregados a protagonistas.
	""" 

	p_bono = models.ForeignKey(ProtagonistaBono, on_delete=models.CASCADE, limit_choices_to=Q(bono__tipo__elemento='plan_inversion'))
	articulo = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='articulos'), related_name='capitalizaciones_articulos')
	unidad = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='unidades'), related_name='capitalizaciones_unidades', help_text='Unidad de Medida')
	cantidad = models.FloatField()
	costo = models.DecimalField('Costo unitario', max_digits=8, decimal_places=2, help_text='Costo en Córdobas(C$)')
	total = models.DecimalField('Costo total', max_digits=10, decimal_places=2, help_text='Costo total en Córdobas(C$)', default=0)
	digitador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='capitalizacion_digitador')
	actualizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='capitalizacion_actualizador')

	class Meta:
		ordering = ['p_bono']


# Tabla de Capacitaciones
class Capacitacion(SoftDeletionModel, TimestampsModel):
	"""
	Clase Capacitacion para registrar las capacitaciones en las
	que han participado los protagonistas.
	""" 

	protagonista = models.ForeignKey(Protagonista, on_delete=models.CASCADE)
	bono = models.ForeignKey(Bono, on_delete=models.RESTRICT, help_text="Bono/Plan correspondiente a la capacitación.")
	tema = models.CharField("Tema de la capacitación", max_length=150)
	comunidad = models.ForeignKey(Comunidad, on_delete=models.RESTRICT, null=True)
	fecha_inicio = models.DateField("Fecha de inicio")
	fecha_final = models.DateField("Fecha de culminación")
	digitador = models.ForeignKey(User, on_delete=models.RESTRICT)

	def __str__(self):
		return "{0} - {1}".format(self.bono.codigo, self.tema.upper())

	class Meta:
		ordering = ['protagonista','fecha_inicio']
		verbose_name = 'Capacitación'
		verbose_name_plural = 'Capacitaciones'


# Tabla de Aportes
class Aporte(SoftDeletionModel, TimestampsModel):
	"""
	Clase Aporte para el registro de los aportes de los protagonistas.
	""" 

	fecha_hora = models.DateTimeField(auto_now_add=True)
	p_bono = models.ForeignKey(ProtagonistaBono, on_delete=models.CASCADE, limit_choices_to={'bono__tipo__elemento':'plan de inversion'})
	tipo = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, help_text='Tipo de aporte')
	mes = models.CharField(
		"Mes",
		max_length=2, 
		choices=[
			('1','ENE'),
			('2','FEB'),
			('3','MAR'),
			('4','ABR'),
			('5','MAY'),
			('6','JUN'),
			('7','JUL'),
			('8','AGO'),
			('9','SEP'),
			('10','OCT'),
			('11','NOV'),
			('12','DIC'),
		]
		)
	anio = models.IntegerField("Año")
	monto = models.DecimalField("Monto C$", max_digits=8, decimal_places=2)
	digitador = models.ForeignKey(User, on_delete=models.RESTRICT)

	def __str__(self):
		return "{0}/{1} - C$ {2}".format(self.mes, self.anio, self.monto)

	class Meta:
		ordering = ['p_bono', 'anio', 'mes']
		



































