from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_timestamps.timestamps import TimestampsModel
from suir.models import Institucion

# Create your models here.

#class Institucion(models.Model):
#	"""docstring for Institucion"""
#	
#	nombre = models.CharField(max_length=50)
#	siglas = models.CharField("Siglas/Acronimo", max_length=15)
#
#	def __str__(self):
#		return self.nombre.upper()
#
#	class Meta:
#		verbose_name_plural = 'Instituciones'


class Funcionario(models.Model):
	"""
	Clase del modelo de datos Funcionario
	"""

	telefono = models.CharField(help_text="Formato: 8888-8888", max_length=9)
	usuario = models.OneToOneField(User, on_delete=models.RESTRICT, limit_choices_to={'is_active':True, 'groups__name__contains':'funcionarios_publicos'})
	institucion = models.ForeignKey(Institucion, on_delete=models.RESTRICT)

	class Meta:
		ordering = ['institucion', 'usuario']

	def __str__(self):
		return "{0} {1}".format(self.usuario.first_name, self.usuario.last_name).upper()


class Beneficiario(models.Model):
	"""docstring for Beneficiario"""
	ETNIA_CHOICES = [
		('M', 'Mestizo'),
		('C', 'Creole'),
		('MK', 'Miskitu'),
		('U', 'Ulwa'),
		('R', 'Rama'),
		('G', 'Garifuna')
	]
	cedula = models.SlugField(max_length=16, primary_key=True)
	primer_nombre = models.CharField(max_length=25)
	segundo_nombre = models.CharField(max_length=25, null=True, blank=True)
	primer_apellido = models.CharField(max_length=25)
	segundo_apellido = models.CharField(max_length=25, null=True, blank=True)
	fecha_nac = models.DateField("Fecha de Nacimiento")
	sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
	etnia = models.CharField(max_length=15, choices=ETNIA_CHOICES)
	direccion = models.TextField(max_length=250, null=True, blank=True)

	def __str__(self):
		return "{0} {1}".format(self.primer_nombre, self.primer_apellido).upper()

	def get_absolute_url(self):
		return reverse('detalle_beneficiario', kwargs={'pk':self.pk})

	class Meta:
		ordering: ['primer_apellido', 'primer_nombre']


class Contribucion(TimestampsModel):
	"""docstring for Contribucion"""
	TIPOS_CONTRIB = [
		('M', 'Monetaria'),
		('Mx', 'Medicinas'),
		('P', 'Provisiones'),
		('Ps', 'Pasajes'),
		('Mt', 'Materiales de Construcción'),
		('A', 'Articulos Escolares'),
		('O', 'Otro'),
	]
	
	fecha = models.DateField()
	beneficiario = models.ForeignKey(Beneficiario, related_name='contribuciones', on_delete=models.RESTRICT)
	tipo = models.CharField(choices=TIPOS_CONTRIB, max_length=2)
	monto = models.DecimalField(max_digits=6, decimal_places=2)
	concepto = models.CharField(max_length=150)
	funcionario = models.ForeignKey(Funcionario, on_delete=models.RESTRICT)
	creado = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{0}>>C$ {1}>>{2}".format(self.fecha, self.monto, self.tipo)

	class Meta:
		ordering = ['-fecha']
		verbose_name_plural = 'Contribuciones'
		
		