

from django.db import models

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
	return True

# --- CRUD Logic Utilities ---
def crud_create(user, table_name, data):
	check_permission(user, table_name, 'create')
	model, serializer_class = ALLOWED_TABLES[table_name]
	# Ensure is_active is set to 1 on create if field exists and is SmallIntegerField
	if 'is_active' in [f.name for f in model._meta.fields]:
		field = model._meta.get_field('is_active')
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			data['is_active'] = 1
		else:
			data['is_active'] = True
	serializer = serializer_class(data=data)
	if serializer.is_valid():
		instance = serializer.save()
		audit_logger.info(f"CREATE {table_name} by {getattr(user, 'username', 'unknown')}: {serializer.data}")
		return Response({
			'success': True,
			'message': 'Record created successfully.',
			'data': serializer.data
		}, status=status.HTTP_201_CREATED)
	return Response({
		'success': False,
		'message': 'Invalid data.',
		'data': serializer.errors
	}, status=status.HTTP_400_BAD_REQUEST)

def crud_list(user, table_name):
	check_permission(user, table_name, 'view')
	model, serializer_class = ALLOWED_TABLES[table_name]
	# Only return active records if is_active field exists
	if hasattr(model, 'is_active') or 'is_active' in [f.name for f in model._meta.fields]:
		field = model._meta.get_field('is_active')
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			queryset = model.objects.filter(is_active=1)
		else:
			queryset = model.objects.filter(is_active=True)
	else:
		queryset = model.objects.all()
	serializer = serializer_class(queryset, many=True)
	return Response({
		'success': True,
		'message': 'Records fetched successfully.',
		'data': serializer.data
	})

# def crud_update(user, table_name, pk, data):
# 	check_permission(user, table_name, 'update')
# 	model, serializer_class = ALLOWED_TABLES[table_name]
# 	try:
# 		instance = model.objects.get(pk=pk)
# 	except model.DoesNotExist:
# 		return Response({
# 			'success': False,
# 			'message': 'Record not found.',
# 			'data': None
# 		}, status=status.HTTP_404_NOT_FOUND)
# 	serializer = serializer_class(instance, data=data, partial=True)
# 	if serializer.is_valid():
# 		serializer.save()
# 		audit_logger.info(f"UPDATE {table_name} id={pk} by {getattr(user, 'username', 'unknown')}: {serializer.data}")
# 		return Response({
# 			'success': True,
# 			'message': 'Record updated successfully.',
# 			'data': serializer.data
# 		})
# 	return Response({
# 		'success': False,
# 		'message': 'Invalid data.',
# 		'data': serializer.errors
# 	}, status=status.HTTP_400_BAD_REQUEST)

def flexible_crud_update(user, table_name, column_name, column_value, data):
	"""
	Enhanced update: Soft delete old record and create new one with updated data
	"""
	check_permission(user, table_name, 'update')
	model, serializer_class = ALLOWED_TABLES[table_name]
	
	# Validate that the column exists in the model
	try:
		field = model._meta.get_field(column_name)
	except:
		return Response({
			'success': False,
			'message': f'Invalid column name: {column_name}',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)
	
	# Find the existing record using the provided column and value
	try:
		lookup_kwargs = {column_name: column_value}
		existing_instance = model.objects.get(**lookup_kwargs, is_active=1)
	except model.DoesNotExist:
		return Response({
			'success': False,
			'message': f'Active record not found with {column_name}={column_value}',
			'data': None
		}, status=status.HTTP_404_NOT_FOUND)
	except model.MultipleObjectsReturned:
		return Response({
			'success': False,
			'message': f'Multiple active records found with {column_name}={column_value}',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)
	
	# Step 1: Soft delete the existing record (set is_active=0)
	if hasattr(existing_instance, 'is_active'):
		field = model._meta.get_field('is_active')
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			setattr(existing_instance, 'is_active', 0)
		else:
			setattr(existing_instance, 'is_active', False)
		existing_instance.save()
		audit_logger.info(f"SOFT DELETE (for update) {table_name} {column_name}={column_value} by {getattr(user, 'username', 'unknown')}")
	else:
		return Response({
			'success': False,
			'message': 'Table does not support soft delete (no is_active field)',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)
	
	# Step 2: Prepare data for new record
	# Include the original column_name and column_value in the new record
	new_data = data.copy()
	new_data[column_name] = column_value
	
	# Ensure is_active is set to 1/True for the new record
	if 'is_active' in [f.name for f in model._meta.fields]:
		field = model._meta.get_field('is_active')
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			new_data['is_active'] = 1
		else:
			new_data['is_active'] = True
	
	# Step 3: Create new record with updated data
	serializer = serializer_class(data=new_data)
	if serializer.is_valid():
		new_instance = serializer.save()
		audit_logger.info(f"CREATE (for update) {table_name} {column_name}={column_value} by {getattr(user, 'username', 'unknown')}: {serializer.data}")
		return Response({
			'success': True,
			'message': 'Record updated successfully (old record archived, new record created).',
			'data': serializer.data
		}, status=status.HTTP_200_OK)
	else:
		# If creation fails, restore the old record
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			setattr(existing_instance, 'is_active', 1)
		else:
			setattr(existing_instance, 'is_active', True)
		existing_instance.save()
		audit_logger.warning(f"RESTORE (update failed) {table_name} {column_name}={column_value} by {getattr(user, 'username', 'unknown')}")
		
		return Response({
			'success': False,
			'message': 'Update failed - invalid data for new record',
			'data': serializer.errors
		}, status=status.HTTP_400_BAD_REQUEST)

def flexible_crud_delete(user, table_name, column_name, column_value):
	"""
	Enhanced delete: Soft delete record using custom column identification
	"""
	check_permission(user, table_name, 'delete')
	model, _ = ALLOWED_TABLES[table_name]
	
	# Validate that the column exists in the model
	try:
		field = model._meta.get_field(column_name)
	except:
		return Response({
			'success': False,
			'message': f'Invalid column name: {column_name}',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)
	
	# Find the existing record using the provided column and value
	try:
		lookup_kwargs = {column_name: column_value}
		instance = model.objects.get(**lookup_kwargs, is_active=1)
	except model.DoesNotExist:
		return Response({
			'success': False,
			'message': f'Active record not found with {column_name}={column_value}',
			'data': None
		}, status=status.HTTP_404_NOT_FOUND)
	except model.MultipleObjectsReturned:
		return Response({
			'success': False,
			'message': f'Multiple active records found with {column_name}={column_value}',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)
	
	# Perform soft delete
	if hasattr(instance, 'is_active'):
		field = model._meta.get_field('is_active')
		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
			setattr(instance, 'is_active', 0)
		else:
			setattr(instance, 'is_active', False)
		instance.save()
		audit_logger.info(f"SOFT DELETE {table_name} {column_name}={column_value} by {getattr(user, 'username', 'unknown')}")
		return Response({
			'success': True,
			'message': 'Record soft deleted successfully.',
			'data': None
		})
	else:
		return Response({
			'success': False,
			'message': 'Soft delete not supported for this table (no is_active field).',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)

# def crud_delete(user, table_name, pk):
# 	check_permission(user, table_name, 'delete')
# 	model, _ = ALLOWED_TABLES[table_name]
# 	try:
# 		instance = model.objects.get(pk=pk)
# 	except model.DoesNotExist:
# 		return Response({
# 			'success': False,
# 			'message': 'Record not found.',
# 			'data': None
# 		}, status=status.HTTP_404_NOT_FOUND)
# 	# Only perform soft delete if is_active exists
# 	if hasattr(instance, 'is_active') or 'is_active' in [f.name for f in model._meta.fields]:
# 		field = model._meta.get_field('is_active')
# 		if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
# 			setattr(instance, 'is_active', 0)
# 		else:
# 			setattr(instance, 'is_active', False)
# 		instance.save()
# 		audit_logger.info(f"SOFT DELETE {table_name} id={pk} by {getattr(user, 'username', 'unknown')}")
# 		return Response({
# 			'success': True,
# 			'message': 'Record soft deleted successfully.',
# 			'data': None
# 		})
# 	else:
# 		return Response({
# 			'success': False,
# 			'message': 'Soft delete not supported for this table.',
# 			'data': None
# 		}, status=status.HTTP_400_BAD_REQUEST)

# # --- Generic CRUD Views ---
# class GenericCreateView(APIView):
# 	authentication_classes = [CustomJWTAuthentication]
# 	permission_classes = [permissions.IsAuthenticated]
# 	def post(self, request):
# 		table_name = request.data.get('table_name')
# 		data = request.data.get('data', {})
# 		if not table_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: table_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if table_name not in ALLOWED_TABLES:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid table name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if not isinstance(data, dict) or not data:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing or invalid data for creation.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		return crud_create(request.user, table_name, data)

# class GenericListView(APIView):
# 	authentication_classes = [CustomJWTAuthentication]
# 	permission_classes = [permissions.IsAuthenticated]
# 	def get(self, request):
# 		table_name = request.query_params.get('table_name')
# 		if not table_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: table_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if table_name not in ALLOWED_TABLES:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid table name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		return crud_list(request.user, table_name)

# class GenericUpdateView(APIView):
# 	authentication_classes = [CustomJWTAuthentication]
# 	permission_classes = [permissions.IsAuthenticated]
# 	def put(self, request, pk):
# 		table_name = request.data.get('table_name')
# 		data = request.data.get('data', {})
# 		if not table_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: table_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if table_name not in ALLOWED_TABLES:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid table name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if not pk:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: id (primary key) for update.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if not isinstance(data, dict) or not data:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing or invalid data for update.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		return crud_update(request.user, table_name, pk, data)

# class GenericDeleteView(APIView):
# 	authentication_classes = [CustomJWTAuthentication]
# 	permission_classes = [permissions.IsAuthenticated]
# 	def delete(self, request, pk):
# 		table_name = request.data.get('table_name')
# 		if not table_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: table_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if table_name not in ALLOWED_TABLES:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid table name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if not pk:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: id (primary key) for delete.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		return crud_delete(request.user, table_name, pk)

# class WrapperAPIView(APIView):
# 	authentication_classes = [CustomJWTAuthentication]
# 	permission_classes = [permissions.IsAuthenticated]

# 	def post(self, request):
# 		table_name = request.data.get('table_name')
# 		method_name = request.data.get('method_name')
# 		data = request.data.get('data', {})
# 		pk = data.get('id')

# 		if not table_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: table_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if table_name not in ALLOWED_TABLES:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid table name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if not method_name:
# 			return Response({
# 				'success': False,
# 				'message': 'Missing required field: method_name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)
# 		if method_name not in ['create', 'list', 'view', 'update', 'delete']:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid method name.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)

# 		if method_name == 'create':
# 			if not isinstance(data, dict) or not data:
# 				return Response({
# 					'success': False,
# 					'message': 'Missing or invalid data for creation.',
# 					'data': None
# 				}, status=status.HTTP_400_BAD_REQUEST)
# 			return crud_create(request.user, table_name, data)
# 		elif method_name == 'list' or method_name == 'view':
# 			return crud_list(request.user, table_name)
# 		elif method_name == 'update':
# 			if not pk:
# 				return Response({
# 					'success': False,
# 					'message': 'Missing required field: id (primary key) for update.',
# 					'data': None
# 				}, status=status.HTTP_400_BAD_REQUEST)
# 			if not isinstance(data, dict) or not data:
# 				return Response({
# 					'success': False,
# 					'message': 'Missing or invalid data for update.',
# 					'data': None
# 				}, status=status.HTTP_400_BAD_REQUEST)
# 			return crud_update(request.user, table_name, pk, data)
# 		elif method_name == 'delete':
# 			if not pk:
# 				return Response({
# 					'success': False,
# 					'message': 'Missing required field: id (primary key) for delete.',
# 					'data': None
# 				}, status=status.HTTP_400_BAD_REQUEST)
# 			return crud_delete(request.user, table_name, pk)
# 		else:
# 			return Response({
# 				'success': False,
# 				'message': 'Invalid request.',
# 				'data': None
# 			}, status=status.HTTP_400_BAD_REQUEST)

class FlexibleWrapperAPIView(APIView):
	"""
	Enhanced wrapper API that supports flexible column-based updates and deletes
	"""
	authentication_classes = [CustomJWTAuthentication]
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		table_name = request.data.get('table_name')
		method_name = request.data.get('method_name')
		column_name = request.data.get('column_name')  # NEW: column to use for identification
		column_value = request.data.get('column_value')  # NEW: value to search for
		data = request.data.get('data', {})

		# Validate required fields
		if not table_name:
			return Response({
				'success': False,
				'message': 'Missing required field: table_name.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)
		
		if table_name not in ALLOWED_TABLES:
			return Response({
				'success': False,
				'message': 'Invalid table name.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)
		
		if not method_name:
			return Response({
				'success': False,
				'message': 'Missing required field: method_name.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)
		
		if method_name not in ['create', 'list', 'view', 'update', 'delete']:
			return Response({
				'success': False,
				'message': 'Invalid method name. Allowed: create, list, view, update, delete',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)

		# Handle different methods
		if method_name == 'create':
			if not isinstance(data, dict) or not data:
				return Response({
					'success': False,
					'message': 'Missing or invalid data for creation.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			return crud_create(request.user, table_name, data)
		
		elif method_name in ['list', 'view']:
			return crud_list(request.user, table_name)
		
		elif method_name == 'update':
			# For update, require column_name and column_value
			if not column_name:
				return Response({
					'success': False,
					'message': 'Missing required field: column_name for update.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			
			if column_value is None:
				return Response({
					'success': False,
					'message': 'Missing required field: column_value for update.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			
			if not isinstance(data, dict) or not data:
				return Response({
					'success': False,
					'message': 'Missing or invalid data for update.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			
			return flexible_crud_update(request.user, table_name, column_name, column_value, data)
		
		elif method_name == 'delete':
			# For delete, require column_name and column_value
			if not column_name:
				return Response({
					'success': False,
					'message': 'Missing required field: column_name for delete.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			
			if column_value is None:
				return Response({
					'success': False,
					'message': 'Missing required field: column_value for delete.',
					'data': None
				}, status=status.HTTP_400_BAD_REQUEST)
			
			return flexible_crud_delete(request.user, table_name, column_name, column_value)
		
		else:
			return Response({
				'success': False,
				'message': 'Invalid request.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)




