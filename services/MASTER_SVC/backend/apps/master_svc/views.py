

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CommandMaster, DepartmentMaster, EquipmentCategoryMaster, ShipCategoryMaster, RoleMaster
from .serializers import (
	CommandMasterSerializer, DepartmentMasterSerializer, EquipmentCategoryMasterSerializer,
	ShipCategoryMasterSerializer, RoleMasterSerializer
)


# --- Generic CRUD Views ---
import logging
from rest_framework.exceptions import PermissionDenied

# Strict whitelist for allowed tables
ALLOWED_TABLES = {
	'tbl_command_master': (CommandMaster, CommandMasterSerializer),
	'tbl_department_master': (DepartmentMaster, DepartmentMasterSerializer),
	'tbl_equipment_category_master': (EquipmentCategoryMaster, EquipmentCategoryMasterSerializer),
	'tbl_ship_category_master': (ShipCategoryMaster, ShipCategoryMasterSerializer),
	'tbl_role_master': (RoleMaster, RoleMasterSerializer),
}

# Audit logger
audit_logger = logging.getLogger('audit')

# Example permission check (replace with real logic)
def check_permission(user, table_name, method_name):
	# TODO: Implement real permission logic per user/table/method
	# Example: Only superusers can delete
	if method_name == 'delete' and not user.is_superuser:
		raise PermissionDenied('You do not have permission to delete.')
	# Add more rules as needed
	return True


class GenericCreateView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request):
		table_name = request.data.get('table_name')
		data = request.data.get('data', {})
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		check_permission(request.user, table_name, 'create')
		model, serializer_class = ALLOWED_TABLES[table_name]
		serializer = serializer_class(data=data)
		if serializer.is_valid():
			instance = serializer.save()
			audit_logger.info(f"CREATE {table_name} by {request.user}: {serializer.data}")
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


class GenericListView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		table_name = request.query_params.get('table_name')
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		check_permission(request.user, table_name, 'view')
		model, serializer_class = ALLOWED_TABLES[table_name]
		queryset = model.objects.all()
		serializer = serializer_class(queryset, many=True)
		return Response(serializer.data)


class GenericUpdateView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def put(self, request, pk):
		table_name = request.data.get('table_name')
		data = request.data.get('data', {})
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		check_permission(request.user, table_name, 'update')
		model, serializer_class = ALLOWED_TABLES[table_name]
		try:
			instance = model.objects.get(pk=pk)
		except model.DoesNotExist:
			return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
		serializer = serializer_class(instance, data=data, partial=True)
		if serializer.is_valid():
			serializer.save()
			audit_logger.info(f"UPDATE {table_name} id={pk} by {request.user}: {serializer.data}")
			return Response(serializer.data)
		return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)


class GenericDeleteView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def delete(self, request, pk):
		table_name = request.data.get('table_name')
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		check_permission(request.user, table_name, 'delete')
		model, _ = ALLOWED_TABLES[table_name]
		try:
			instance = model.objects.get(pk=pk)
			instance.delete()
			audit_logger.info(f"DELETE {table_name} id={pk} by {request.user}")
			return Response({'success': True})
		except model.DoesNotExist:
			return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

# --- Wrapper API ---

class WrapperAPIView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		table_name = request.data.get('table_name')
		method_name = request.data.get('method_name')
		data = request.data.get('data', {})
		pk = data.get('id')

		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		if method_name not in ['create', 'list', 'view', 'update', 'delete']:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			check_permission(request.user, table_name, method_name)
		except PermissionDenied:
			return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

		if method_name == 'create':
			return GenericCreateView.as_view()(request)
		elif method_name == 'list' or method_name == 'view':
			request.GET = request.GET.copy()
			request.GET['table_name'] = table_name
			return GenericListView.as_view()(request)
		elif method_name == 'update':
			if not pk:
				return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
			return GenericUpdateView.as_view()(request, pk=pk)
		elif method_name == 'delete':
			if not pk:
				return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
			return GenericDeleteView.as_view()(request, pk=pk)
		else:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)




