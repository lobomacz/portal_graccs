from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.decorators import action
from hamster.permissions import IsOwnerOrReadOnly
from hamster.serializers import *
from hamster.models import *
import json



# Create your views here.


class ContribucionViewSet(viewsets.ModelViewSet):

	""" 
	Este viewset gestiona las operaciones CRUD de Contribuciones
	""" 

	queryset = Contribucion.objects.all()
	serializer_class = ContribucionSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

	@action(detail=True)
	def por_beneficiario(self, request, pk=None):
		contribuciones = self.get_queryset().filter(beneficiario=pk)
		serializer = self.get_serializer(contribuciones, many=True)
		return Response(serializer.data)


	@action(detail=False)
	def count(self, request):
		cuenta = self.get_queryset().count()
		datos = json.dumps({'count':cuenta})
		return Response(datos)


	def perform_create(self, serializer):
		serializer.save(funcionario=self.request.user.funcionario)


		
class BeneficiarioViewSet(viewsets.ModelViewSet):

	"""
	Este viewset gestiona las operaciones CRUD de Beneficiario
	"""

	queryset = Beneficiario.objects.all()
	serializer_class = BeneficiarioSerializer
	permission_classes = [permissions.IsAuthenticated]


	@action(detail=False)
	def count(self, request):
		cuenta = self.get_queryset().count()
		datos = json.dumps({'count':cuenta})
		return Response(datos)

				

class FuncionarioViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	Este viewset va a gestionar las consultas de Funcionarios
	""" 
	queryset = Funcionario.objects.all()
	serializer_class = FuncionarioSerializer
	permission_classes = [permissions.IsAuthenticated]




class InstitucionViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	Este viewset gestiona las consultas de Institución.
	"""

	queryset = Institucion.objects.all()
	serializer_class = InstitucionSerializer
	permission_classes = [permissions.IsAuthenticated]
	
	


class UserLogin(APIView):

	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]


	def post(self, request, format=None):

		uname = request.data['username']
		pword = request.data['password']

		user = authenticate(username=uname, password=pword)
		if user is not None:
			serializer = UserSerializer(user)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








		


		
