from django.contrib.gis.db import models
from django.db.models import Q
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django_timestamps.softDeletion import SoftDeletionModel
from django_timestamps.timestamps import TimestampsModel
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.


class Anuncio(models.Model):
        """Clase del modelo Anuncio"""
        titulo = models.CharField('Título', max_length=45)
        imagen = models.ImageField('Imágen', upload_to='suir/anuncios/img/')
        url = models.URLField('URL del sitio', max_length=150)
        activo = models.BooleanField()

        def __str__(self):
                return self.titulo

        class Meta:
                ordering = ['activo', 'titulo']



class Carrusel(SoftDeletionModel):
        """ 
        Modelo Carrusel. Se emplea para administrar las imágenes que se despliegan en el carrusel.
        """

        imagen = models.ImageField(upload_to='suir/carrusel/img/')
        titulo = models.CharField(max_length=25)
        descripcion = models.CharField(max_length=250)
        activo = models.BooleanField()

        class Meta:
                ordering = ['activo', 'titulo']

        def __str__(self):
                return self.titulo
        
        

class Contacto(SoftDeletionModel):
        """Clase del modelo Contacto"""
        nombre = models.CharField(max_length=50)
        apellido = models.CharField(max_length=50)
        movil = models.CharField('Móvil', max_length=9, validators=[RegexValidator(regex="[0-9]{4}-[0-9]{4}", message="El valor no es un número telefónico válido.")], help_text="Formato 8888-8888")
        correo = models.EmailField('Correo electrónico')
        cargo = models.ForeignKey('DetalleTabla', on_delete=models.SET_NULL, limit_choices_to=Q(tabla__tabla='cargos'), null=True)
        institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)

        def __str__(self):
                return "%s %s" % (self.nombre, self.apellido)

        class Meta:
                ordering = ['institucion', 'apellido']



class Tabla(TimestampsModel):
        """Clase para el modelo Tabla"""
        tabla = models.CharField(max_length=25)

        def __str__(self):
                return self.tabla.upper()



class DetalleTabla(TimestampsModel):
        """Clase para el modelo DetalleTabla"""
        elemento = models.CharField(max_length=45)
        codigo_eq = models.CharField('Código de equivalencia', max_length=15, null=True, blank=True)
        tabla = models.ForeignKey(Tabla, on_delete=models.CASCADE)

        def __str__(self):
                return self.elemento.upper()

        class Meta:
                ordering = ['tabla', 'id']

        
                
class Entidad(SoftDeletionModel):
        """Clase para el modelo Entidad de Monitoreo de Indicadores"""
        nombre = models.CharField(max_length=45)
        sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), help_text="Sector social que atiende la entidad.")
        nivel = models.CharField(max_length=45, choices=[('S', 'SECRETARÍA'),('D', 'DIRECCIÓN'),('C', 'COMISIÓN'), ('O', 'OFICINA')])
        enlace = models.BooleanField('Es Enlace')

        def __str__(self):
                return self.nombre

        class Meta:
                verbose_name_plural = 'Entidades'


class Municipio(models.Model):

        """
        Clase para el modelo Municipio.
        """ 
        nombre = models.CharField(max_length=50)
        nombre_corto = models.CharField(max_length=10)
        region = models.CharField(max_length=5, choices=[('racs', 'Región Autónoma del Caribe Sur'),('racn', 'Región Autónoma del Caribe Norte')], default='racs')
        area = models.FloatField('Área (Km2)', null=True, help_text="Extensión en Km2")
        poblacion = models.IntegerField('Población aprox.', null=True)

        mpoly = models.MultiPolygonField()

        def __str__(self):
                return self.nombre.upper()

        class Meta:
                ordering = ['nombre']


class Comunidad(models.Model):

        """ 
        Clase para el modelo Comunidad. Empleado como nivel por defecto de desagregación de indicadores.
        """
        nombre = models.CharField(max_length=150)
        municipio = models.ForeignKey(Municipio, on_delete=models.RESTRICT)
        actividades_ec = models.ManyToManyField(DetalleTabla, related_name='+', help_text='Actividades económicas desarrolladas en la comunidad.', limit_choices_to=Q(tabla__tabla='actividades_ec'))

        location = models.PointField(null=True)

        def __str__(self):
                return "%s-%s" % (self.municipio.nombre_corto.upper(), self.nombre.upper())

        class Meta:
                verbose_name_plural = 'Comunidades'
                ordering = ['municipio', 'nombre']



class Indicador(SoftDeletionModel, TimestampsModel):
        """Clase para el modelo Indicador"""
        
        titulo = models.CharField('Título', max_length=150)     
        descripcion = models.CharField(max_length=250)
        sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), help_text="Sector social al que pertenece el indicador.", related_name='indicadores_sectores', related_query_name='indicador_sector')
        formula = models.CharField('Fórmula de Cálculo', max_length=50, help_text="Fórmula con la que se calcula el valor del indicador.")
        metrica = models.CharField('Métrica de Valoración', max_length=25, choices=[('Cre', 'Creciente'), ('Dec', 'Decreciente')], help_text="Métrica con que se analizan los valores del indicador.")
        tipo_valor = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, limit_choices_to=Q(tabla__tabla='tipos_valor'), null=True, related_name='indicadores_tipos_valores', related_query_name='indicador_tipo_valor', help_text='Tipo de valor del indicador.')
        periodicidad = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, limit_choices_to=Q(tabla__tabla='periodos'), null=True, related_name='indicadores_periodos', related_query_name='indicador_periodo')
        portada = models.ImageField('Portada', upload_to='suir/indicadores/img/', null=True)
        ficha = models.FileField('Ficha Técnica', upload_to='suir/indicadores/docs/', help_text="Documento en Formato PDF", null=True, blank=True)
        tags = models.TextField(null=True, blank=True)
        entidad = models.ForeignKey(Entidad, on_delete=models.RESTRICT, help_text='Entidad responsable del seguimiento del indicador.')
        colaboradores = models.ManyToManyField('Institucion', help_text='Instituciones colaboradoras en la recolección de datos para el indicador.')
        responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='indicadores_responsables', related_query_name='indicador_responsable')
        desagregaciones = models.ManyToManyField(DetalleTabla, help_text='Desagregaciones del indicador', related_name='+', limit_choices_to=Q(tabla__tabla='desagregaciones'))
        fuente = models.CharField('Fuente de datos', max_length=150, help_text="Fuente donde se obtienen los datos/valores del indicador.")
        marco = models.CharField('Marco legal', max_length=150, help_text="Marco legal que respalda el seguimiento del indicador.")
        estado = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, limit_choices_to=Q(tabla__tabla='estados_pub'), help_text="Posibles valores: borrador, pendiente, publicado", null=True, related_name='indicadores_estados', related_query_name='indicador_estado')
        version = models.PositiveSmallIntegerField()
        activo = models.BooleanField()
        seguimiento = models.BooleanField('En seguimiento', help_text='El indicador está siendo monitoreado y se recogen datos del mismo.')
        creador = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='indicadores_creadores', related_query_name='indicador_creador')

        def __str__(self):
                return self.titulo.upper()

        def get_absolute_url(self):
                return reverse('detalle_indicador', kwargs={'pk':self.pk})

        class Meta:
                ordering = ['-seguimiento', 'sector', 'titulo']
                verbose_name_plural = 'Indicadores'



class ValorIndicador(SoftDeletionModel, TimestampsModel):
        """Clase del modelo ValorIndicador""" 
        fecha = models.DateField('Fecha', auto_now_add=True)
        fecha_inicio = models.DateField('Inicio de la captación')
        fecha_final = models.DateField('Final de la captación')
        indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, limit_choices_to={'activo':True, 'seguimiento':True})
        recolector = models.CharField('Recolector de datos', max_length=50)
        entidad = models.ForeignKey(Entidad, on_delete=models.RESTRICT)
        digitador = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='valores_digitadores', related_query_name='valor_digitador')
        supervisor = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='valores_supervisores', related_query_name='valor_supervisor')
        codigo_ficha = models.CharField('Código de ficha', max_length=50, null=True, blank=True)
        ficha = models.FileField(upload_to='suir/indicadores/fichas/', help_text='Ficha en formato PDF', null=True, blank=True)
        comunidad = models.ForeignKey(Comunidad, on_delete=models.RESTRICT, default=1, help_text='Comunidad donde se levantó el dato.')
        sexo = models.CharField('Sexo', max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], null=True, blank=True, help_text='Si aplica al tipo de valor del indicador.')
        etnia = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, null=True, blank=True, related_name='valores_etnias', related_query_name='valor_etnia')
        rango_edad = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, help_text='Rango de edad (si aplica).', null=True, related_name='valores_rangos_edad', related_query_name='valor_rango_edad')
        valor = models.DecimalField('Valor', max_digits=8, decimal_places=2)
        estado = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, help_text="Posibles valores: borrador, pendiente, publicado", related_name='valores_estados', related_query_name='valor_estado')

        class Meta:
                ordering = ['indicador', '-fecha']
                verbose_name = 'Valor'
                verbose_name_plural = 'Valores'

        def get_absolute_url(self):
                return reverse('detalle_valor_indicador', kwargs={'pk':self.pk})



class Institucion(models.Model):
        """Clase del modelo Institucion"""
        nombre = models.CharField(max_length=150)
        siglas = models.CharField(max_length=15)
        url = models.URLField(max_length=100, null=True, blank=True)
        sector = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, limit_choices_to=Q(tabla__tabla='sectores'), help_text="Sector social que atiende la institución", related_name='instituciones_sectores', related_query_name='institucion_sector')

        def __str__(self):
                return self.nombre.upper()

        class Meta:
                ordering = ['nombre']
                verbose_name = 'Institución'
                verbose_name_plural = 'Instituciones'



class LinkExterno(SoftDeletionModel, TimestampsModel):
        """Clase del modelo Link Externo"""
        texto = models.CharField(max_length=15, help_text='Texto del enlace')
        url = models.URLField(max_length=150, help_text='URL al que apunta el enlace')
        descripcion = models.CharField(max_length=50, help_text='Descripción del enlace', null=True, blank=True)
        activo = models.BooleanField(default=True)

        def __str__(self):
                return self.texto

        class Meta:
                ordering = ['-activo']
                verbose_name = 'Enlace externo'
                verbose_name_plural = 'Enlaces externos'



class LinkRed(SoftDeletionModel):
        """
        Clase del modelo Link Red. Se emplea para registrar los enlaces a redes sociales.
        """ 
        red = models.CharField(max_length=25, choices=[('facebook', 'Facebook'),('twitter', 'Twitter'),('instagram', 'Instagram'),('youtube', 'YouTube')])
        url = models.URLField(max_length=150, help_text='URL de la red social.')
        activo = models.BooleanField(default=True)

        class Meta:
                verbose_name_plural = 'LinkRedes'

        def __str__(self):
                return self.red.upper()



class Publicacion(SoftDeletionModel, TimestampsModel):
        """Clase del modelo Publicacion"""
        titulo = models.CharField('Título', max_length=250)
        slug = models.SlugField(max_length=150)
        fecha = models.DateField()
        autor = models.ForeignKey(User, on_delete=models.RESTRICT)
        portada = models.ImageField(upload_to='suir/publicaciones/img/')
        contenido = RichTextUploadingField(
                config_name='default', 
                extra_plugins=[
                'autolink',
        'autoembed',
        'clipboard',
        'dialog',
        'dialogui',
        'embedsemantic',
        'image2',
        'iframe',
        'iframedialog',
        'language',
        'uploadimage',
        'widget',
        'youtube',
                ],
                external_plugin_resources=[
                        (
                        'youtube', 
                        '/static/suir/plugins/youtube/youtube/',
                        'plugin.js',
                        )
                ])
        documento = models.FileField(upload_to='suir/publicaciones/docs/', null=True, blank=True)
        tags = models.TextField('Etiquetas', null=True, blank=True, help_text='Etiquetas separadas por coma.')
        tipo = models.ForeignKey(DetalleTabla, on_delete=models.SET_NULL, null=True, related_name='publicaciones_tipos', related_query_name='publicacion_tipo')
        estado = models.ForeignKey(DetalleTabla, on_delete=models.RESTRICT, help_text="Posibles valores: borrador, pendiente, publicado", related_name='publicaciones_estados', related_query_name='publicacion_estado')
        carrusel = models.BooleanField('Promovido al carrusel', default=False)
        publicado = models.DateField('Fecha publicado', null=True, blank=True, help_text="Fecha de publicación")

        def __str__(self):
                return self.titulo.upper()

        def get_absolute_url(self):
                if self.tipo.elemento == 'noticia':
                        return reverse('detalle_noticia', kwargs={'slug':self.slug})
                else:
                        return reverse('detalle_informe', kwargs={'slug':self.slug})


        class Meta:
                permissions = [
                ('crear_noticia', 'Redacta Noticias'),
                ('crear_informe', 'Redacta Informes'),
                ('publicar_noticia', 'Publica Noticias'),
                ('publicar_informe', 'Publica Informes')
                ]
                ordering = ['tipo', 'estado', '-fecha', 'autor']
                verbose_name = 'Publicación'
                verbose_name_plural = 'Publicaciones'


class Transmision(TimestampsModel):

        """ Modelo de transmisiones de YouTube """

        descripcion = models.CharField('Descripción', max_length=200, help_text='Campo empleado para la interfaz administrativa.')
        inicio = models.DateTimeField('Hora de Inicio', auto_now_add=True)
        final = models.DateTimeField('Hora de Culminación', null=True, blank=True)
        codigo = models.TextField('Código </>', validators=[RegexValidator(regex=r"<iframe", message="El campo debe contener el código <embed>.")], help_text='Código Embed/Insertar </> de la transmisión.', null=True, blank=True)
        origen = models.CharField(max_length=2, choices=[('yt', 'YouTube'), ('fb', 'Facebook')], default='yt')
        especial = models.BooleanField('Transmisión Especial', help_text='Seleccionar en caso que la transmisión no corresponda al noticiero RBS.', default=False)
        publicador = models.ForeignKey(User, on_delete=models.RESTRICT)

        class Meta:
                verbose_name = 'Transmisión'
                verbose_name_plural = 'Transmisiones'
                ordering = ['inicio']
                get_latest_by = 'inicio'

        def __str__(self):
                return self.descripcion.upper()
