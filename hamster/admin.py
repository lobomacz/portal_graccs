from django.contrib.admin import AdminSite, ModelAdmin, TabularInline
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from hamster.models import Funcionario, Beneficiario, Contribucion


# Register your models here.

class HamsterAdmin(AdminSite):

	site_header = 'Administración Hamster App'
	site_title = 'Hamster Admin'
	index_title = site_title
	site_url = '/hamster/'

class ContribucionInline(TabularInline):
	model = Contribucion
	ordering = ['fecha', 'beneficiario']

class FuncionarioAdmin(ModelAdmin):
	inlines = [
		ContribucionInline,
	]

class BeneficiarioAdmin(ModelAdmin):
	model = Beneficiario

class UsuarioAdmin(UserAdmin):
	model = User
