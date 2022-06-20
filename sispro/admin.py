from django.contrib.admin.sites import AdminSite
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from rest_framework.authtoken.admin import TokenAdmin
from django.urls import reverse
from sispro.models import *

# Register your models here.

TokenAdmin.raw_id_fields = ['user']

class SisproAdminSite(AdminSite):
	site_header = 'Admin SISPRO'
	site_title = site_header
	site_url = '/sispro/'
	index_title = site_title


class ProyectoInline(StackedInline):
	ordering = ['programa', 'codigo']
	model = Proyecto


class ProgramaAdmin(ModelAdmin):
	ordering = ['codigo']
	inlines = [
		ProyectoInline,
	]

class ProtagonistaAdmin(ModelAdmin):
	ordering = ['comunidad__municipio__nombre', 'comunidad__nombre', 'apellidos']
	exclude = ['deleted_at']

	def save_model(self, request, obj, form, change):
		obj.cedula = obj.cedula.replace('-', '').strip().upper()
		super().save_model(request, obj, form, change)


class TecnicoAdmin(ModelAdmin):
	ordering = ['comunidad__municipio__nombre', 'comunidad__nombre', 'apellidos']
	exclude = ['deleted_at']

	def save_model(self, request, obj, form, change):
		obj.cedula = obj.cedula.replace('-', '').strip().upper()
		super().save_model(request, obj, form, change)




