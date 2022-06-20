from django.urls import include, path
#from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from hamster.views import *

# Creamos un router para los viewsets utilizados en la API

router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet)
router.register(r'funcionarios', FuncionarioViewSet)
router.register(r'beneficiarios', BeneficiarioViewSet)
router.register(r'contribuciones', ContribucionViewSet)


urlpatterns = [
	path('auth/', UserLogin.as_view(), name='user_login'),
	path('', include(router.urls)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)