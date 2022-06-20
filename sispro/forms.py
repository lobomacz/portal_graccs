from django import forms
from django.forms import Form, ModelForm, inlineformset_factory
from sispro.models import Protagonista,ProtagonistaBono,CapitalizacionBono


# Formulario de autenticación
class LoginForm(Form):
	nombreusuario = forms.CharField(max_length=25,label='Nombre de Usuario')
	contrasena = forms.CharField(max_length=25,widget=forms.PasswordInput,label='Contraseña') 



# Formulario de edición de Protagonistas
class ProtagonistaForm(ModelForm):

	class Meta:
		model = Protagonista
		fields = ['cedula','nombres','apellidos','fecha_nacimiento','sexo','etnia','comunidad','telefono','promotor','jvc']
		widgets = {
			'cedula':forms.TextInput(attrs={'readonly':True})
		}


# Formulario de ingreso y edición de entrega de Bonos/Planes de Inversión
class ProtagonistaBonoForm(ModelForm):

	class Meta:
		model = ProtagonistaBono
		fields = [
		'protagonista',
		'bono',
		'proyecto',
		'fecha_recibido',
		'tecnico',
		'comunidad',
		'coord_x',
		'coord_y',
		'altura',
		'observaciones'
		]
		widgets = {
			'fecha_recibido':forms.DateInput()
		}


# Formulario para uso de inlineformset junto con el formulario ProtagonistaBonoForm
class CapitalizacionBonoForm(ModelForm):

	class Meta:
		model = CapitalizacionBono
		exclude = ['protagonista_bono']


CapitalizacionBonoFormset = inlineformset_factory(ProtagonistaBono, CapitalizacionBono, form=CapitalizacionBonoForm, extra=20)
CapitalizacionBonoFormset2 = inlineformset_factory(ProtagonistaBono, CapitalizacionBono, form=CapitalizacionBonoForm, extra=4)

