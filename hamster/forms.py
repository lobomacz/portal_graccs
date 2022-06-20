from django import forms 
from hamster.models import Contribucion, Beneficiario 

class FormContribucion(forms.ModelForm):
	"""
	Formulario del modelo Contribucion
	"""
	class Meta:
		fields = '__all__'
		model = Contribucion


class FormBeneficiario(forms.ModelForm):
	"""
	Formulario del modelo Beneficiario
	"""
	class Meta:
		fields = '__all__'
		model = Beneficiario



class FormLogin(forms.Form):
	"""
	Formulario de validación de usuario
	"""
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=25)
		
