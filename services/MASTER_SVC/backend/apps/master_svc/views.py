

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .authentication import CustomJWTAuthentication

# import all master models
from .models import (
	CommandMaster, DepartmentMaster, EquipmentCategoryMaster,
	ShipCategoryMaster, RoleMaster, ShipStateMaster,
	ShipLocationMaster, ActivityTypeMaster, ActivityDetailsMaster,
	LubricantMaster
)

# import all master serializers
from .serializers import (
	CommandMasterSerializer, DepartmentMasterSerializer, EquipmentCategoryMasterSerializer,
	ShipCategoryMasterSerializer, RoleMasterSerializer, ShipStateMasterSerializer,
	ShipLocationMasterSerializer, ActivityTypeMasterSerializer, ActivityDetailsMasterSerializer,
	LubricantMasterSerializer
)



# --- Generic CRUD Views ---

import logging
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

# Strict whitelist for allowed tables
ALLOWED_TABLES = {
    #remaining Master Tables
	'tbl_command_master': (CommandMaster, CommandMasterSerializer),
	'tbl_department_master': (DepartmentMaster, DepartmentMasterSerializer),
	'tbl_equipment_category_master': (EquipmentCategoryMaster, EquipmentCategoryMasterSerializer),
	'tbl_ship_category_master': (ShipCategoryMaster, ShipCategoryMasterSerializer),
	'tbl_role_master': (RoleMaster, RoleMasterSerializer),
 
    # --- SRAR Master Tables ---
	'tbl_ship_state_master': (ShipStateMaster, ShipStateMasterSerializer),
	'tbl_ship_location_master': (ShipLocationMaster, ShipLocationMasterSerializer),
	'tbl_activity_type_master': (ActivityTypeMaster, ActivityTypeMasterSerializer),
	'tbl_activity_details_master': (ActivityDetailsMaster, ActivityDetailsMasterSerializer),
	'tbl_lubricant_master': (LubricantMaster, LubricantMasterSerializer),
}

# Audit logger
audit_logger = logging.getLogger('audit')

# Example permission check (replace with real logic)
def check_permission(user, table_name, method_name):
	if method_name == 'delete' and not getattr(user, 'is_superuser', False):
		raise PermissionDenied('You do not have permission to delete.')
	return True

# --- CRUD Logic Utilities ---
def crud_create(user, table_name, data):
	check_permission(user, table_name, 'create')
	model, serializer_class = ALLOWED_TABLES[table_name]
	serializer = serializer_class(data=data)
	if serializer.is_valid():
		instance = serializer.save()
		audit_logger.info(f"CREATE {table_name} by {getattr(user, 'username', 'unknown')}: {serializer.data}")
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)

def crud_list(user, table_name):
	check_permission(user, table_name, 'view')
	model, serializer_class = ALLOWED_TABLES[table_name]
	queryset = model.objects.all()
	serializer = serializer_class(queryset, many=True)
	return Response(serializer.data)

def crud_update(user, table_name, pk, data):
	check_permission(user, table_name, 'update')
	model, serializer_class = ALLOWED_TABLES[table_name]
	try:
		instance = model.objects.get(pk=pk)
	except model.DoesNotExist:
		return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
	serializer = serializer_class(instance, data=data, partial=True)
	if serializer.is_valid():
		serializer.save()
		audit_logger.info(f"UPDATE {table_name} id={pk} by {getattr(user, 'username', 'unknown')}: {serializer.data}")
		return Response(serializer.data)
	return Response({'error': 'Invalid data.'}, status=status.HTTP_400_BAD_REQUEST)

def crud_delete(user, table_name, pk):
	check_permission(user, table_name, 'delete')
	model, _ = ALLOWED_TABLES[table_name]
	try:
		instance = model.objects.get(pk=pk)
		instance.delete()
		audit_logger.info(f"DELETE {table_name} id={pk} by {getattr(user, 'username', 'unknown')}")
		return Response({'success': True})
	except model.DoesNotExist:
		return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

# --- Generic CRUD Views ---
class GenericCreateView(APIView):
	authentication_classes = [CustomJWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request):
		table_name = request.data.get('table_name')
		data = request.data.get('data', {})
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		return crud_create(request.user, table_name, data)

class GenericListView(APIView):
	authentication_classes = [CustomJWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request):
		table_name = request.query_params.get('table_name')
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		return crud_list(request.user, table_name)

class GenericUpdateView(APIView):
	authentication_classes = [CustomJWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def put(self, request, pk):
		table_name = request.data.get('table_name')
		data = request.data.get('data', {})
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		return crud_update(request.user, table_name, pk, data)

class GenericDeleteView(APIView):
	authentication_classes = [CustomJWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]
	def delete(self, request, pk):
		table_name = request.data.get('table_name')
		if table_name not in ALLOWED_TABLES:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
		return crud_delete(request.user, table_name, pk)

class WrapperAPIView(APIView):
	authentication_classes = [CustomJWTAuthentication]
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

		if method_name == 'create':
			return crud_create(request.user, table_name, data)
		elif method_name == 'list' or method_name == 'view':
			return crud_list(request.user, table_name)
		elif method_name == 'update':
			if not pk:
				return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
			return crud_update(request.user, table_name, pk, data)
		elif method_name == 'delete':
			if not pk:
				return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
			return crud_delete(request.user, table_name, pk)
		else:
			return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)




