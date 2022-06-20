from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	Clase para definir permiso de modificación o eliminar
	a digitadores propietarios de contribuciones.
	"""

	def has_object_permissions(self, request, view, obj):
		# Los permisos de lectura son permitidos para cualquier solicitud.
		# Así que se permitirán solicitudes GET, HEAD y OPTIONS.

		if request.method in permissions.SAFE_METHODS:
			return True

		# Los permisos de escritura se darán solamente al digitador propietario
		return request.user == obj.digitador