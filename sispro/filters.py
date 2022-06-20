from django_filters import rest_framework as filters
from sispro.models import Protagonista


# Definimos FilterSets para los ViewSets que apliquen DefaultFilterBackend

class ProtagonistaFilter(filters.FilterSet):

	

	class Meta:
		model = Protagonista
		fields
