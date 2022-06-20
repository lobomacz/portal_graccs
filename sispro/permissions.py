from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Clase para definir los controles en los viewsets
	""" 

	def has_object_permissions(self, request, view, obj):
		
		if request.method in permissions.SAFE_METHODS:
			return True


		return request.user == obj.digitador

