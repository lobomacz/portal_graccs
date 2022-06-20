from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import View 
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from hitcount.views import HitCountDetailView
from suir.models import *
import datetime


# Create your views here.

PAGINAS = settings.SUIR_CONF['paginas']


# Views

class InicioView(TemplateView):

	template_name = 'suir/inicio.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)

		carrusel = Carrusel.objects.filter(activo=True)
		promovidos = Publicacion.objects.filter(carrusel=True)

		min_count = 3
		max_count = 6
		car_count = carrusel.count()
		prom_count = promovidos.count()

		if prom_count > min_count and car_count > min_count:
			carrusel = carrusel.order_by('-id')[:min_count]
			promovidos = promovidos.order_by('-fecha')[:min_count]
		elif prom_count > car_count and car_count <= min_count:
			promovidos = promovidos.order_by('-fecha')[:max_count]
		else:
			carrusel = carrusel.order_by('-id')[:max_count]

		anuncios = Anuncio.objects.filter(activo=True).order_by('-id')[:2]
		noticias = Publicacion.objects.filter(tipo__elemento='noticia', estado__elemento='publicado')[:4]
		informes = Publicacion.objects.filter(tipo__elemento='informe', estado__elemento='publicado')[:4]
		enlaces = LinkExterno.objects.filter(activo=True)[:6]
		redes = LinkRed.objects.filter(activo=True)
		transmision = None

		try:
			transmision = Transmision.objects.latest('inicio')
			tduracion = datetime.timedelta(hours=1)
			tactual = timezone.now()
			print(tactual.tzinfo.utcoffset(None))

			if transmision.final != None:
				if transmision.final < tactual:
					transmision = None 
			else:
				ttranscurrido = transmision.inicio + tduracion
				if ttranscurrido < tactual:
					transmision = None 
		except Transmision.DoesNotExist as e:
			print(e)
			transmision = None
		finally:
			context['transmision'] = transmision

		context['carrusel'] = carrusel
		context['promovidos'] = promovidos
		context['anuncios'] = anuncios
		context['noticias'] = noticias
		context['informes'] = informes
		context['enlaces'] = enlaces
		context['redes'] = redes 
		context['carrusel_count'] = car_count + prom_count
		context['fecha'] = datetime.datetime.now()

		return context


class SuirListView(ListView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context['paginator']

		enlaces = LinkExterno.objects.filter(activo=True)[:6]
		redes = LinkRed.objects.filter(activo=True)

		context['enlaces'] = enlaces
		context['redes'] = redes 

		context['fecha'] = datetime.datetime.now()

		context['rango_paginas'] = paginator.get_elided_page_range(self.request.GET.get('page',1), on_each_side=3, on_ends=3)

		return context


class SuirDetailView(DetailView):

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		enlaces = LinkExterno.objects.filter(activo=True)[:6]
		redes = LinkRed.objects.filter(activo=True)

		context['enlaces'] = enlaces
		context['redes'] = redes 

		context['fecha'] = datetime.datetime.now()

		return context



class ListaPublicacionesView(SuirListView):
	paginate_by = PAGINAS
	template_name = 'suir/grid_list.html'
	tipo = ''

	def get_queryset(self):
		return Publicacion.objects.filter(tipo__elemento=self.tipo, estado__elemento='publicado')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = self.tipo
	
		return context


class ListaFiltroPublicacionesView(ListaPublicacionesView):

	def get_queryset(self):
		clave = self.request.GET.get('q').strip()

		return Publicacion.objects.filter(Q(titulo__contains=clave) | Q(tags__contains=clave),tipo__elemento=self.tipo, estado__elemento='publicado')


class DetallePublicacionView(HitCountDetailView):
	model = Publicacion
	context_object_name = 'publicacion'
	count_hit = True

	def get_queryset(self):
		slug = self.kwargs['slug']
		return Publicacion.objects.filter(slug=slug)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		enlaces = LinkExterno.objects.filter(activo=True)[:6]
		redes = LinkRed.objects.filter(activo=True)

		context['tipo'] = self.object.tipo.elemento
		context['tags'] = [tag.strip() for tag in  self.get_object().tags.split(',')]
		context['enlaces'] = enlaces
		context['redes'] = redes 
		context['fecha'] = datetime.datetime.now()

		return context




class ListaIndicadoresView(SuirListView):
	paginate_by = PAGINAS
	model = Indicador

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = 'indicador'
		return context


class ListaFiltroIndicadoresView(ListaIndicadoresView):

	def get_queryset(self):
		clave = self.request.GET.get('q').strip()
		return Indicador.objects.filter(Q(titulo__contains=clave) | Q(sector__elemento__startswith=clave) | Q(tags__contains=clave))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = 'indicador'
		return context


class DetalleIndicadorView(SuirDetailView):
	model = Indicador
	context_object_name = 'indicador'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['tipo'] = 'indicador'
		return context


class DetalleValorView(LoginRequiredMixin, SuirDetailView):

	model = ValorIndicador
	context_object_name = 'valor'





