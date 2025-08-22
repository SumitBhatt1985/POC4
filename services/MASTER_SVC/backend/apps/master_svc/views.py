import logging
from rest_framework.exceptions import PermissionDenied

from rest_framework import permissions, status
from rest_framework.views import APIView
from django.db import models
from rest_framework import permissions, status
from rest_framework.response import Response
from .authentication import CustomJWTAuthentication
# from django.db.models import F  

# import all master models
from .models import (
	CommandMaster, DepartmentMaster, EquipmentCategoryMaster,
	ShipCategoryMaster, RoleMaster, ShipStateMaster,
	ShipLocationMaster, ActivityTypeMaster, ActivityDetailsMaster,
	LubricantMaster, SectionMaster, GroupMaster, CountryMaster,
	ClassMaster, SupplierMaster, OpsAuthorityMaster,
	GenericMaster, EstablishmentMaster, PropulsionMaster,
	ManufacturerMaster, EquipmentMaster, ShipMaster,
 
	VwSectionDepartment, VwSectionGroupDetails, VwCountrySupplierDetails, VwActivityTypeDetails, 
 	VwCommandOpsauthorityDetails, VwCommandOpsauthorityEstablishmentDetails, 
  	VwCountryManufacturerDetails, VwSectionEquipmentGroupDetails
)

# import all master serializers
from .serializers import (
	CommandMasterSerializer, DepartmentMasterSerializer, EquipmentCategoryMasterSerializer,
	ShipCategoryMasterSerializer, RoleMasterSerializer, ShipStateMasterSerializer,
	ShipLocationMasterSerializer, ActivityTypeMasterSerializer, ActivityDetailsMasterSerializer,
	LubricantMasterSerializer, SectionMasterSerializer, GroupMasterSerializer, CountryMasterSerializer,
	ClassMasterSerializer, SupplierMasterSerializer, OpsAuthorityMasterSerializer,
	GenericMasterSerializer, EstablishmentMasterSerializer, PropulsionMasterSerializer,
	ManufacturerMasterSerializer, EquipmentMasterSerializer, ShipMasterSerializer,
	
	VwSectionDepartmentSerializer, VwSectionGroupDetailsSerializer, VwCountrySupplierDetailsSerializer, VwActivityTypeDetailsSerializer, 
  	VwCommandOpsauthorityDetailsSerializer, VwCommandOpsauthorityEstablishmentDetailsSerializer, 
    VwCountryManufacturerDetailsSerializer, VwSectionEquipmentGroupDetailsSerializer
)

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

	# --- SFD Master Tables ---
	'tbl_section_master' : (SectionMaster, SectionMasterSerializer),
	'tbl_group_master' : (GroupMaster, GroupMasterSerializer),
	'tbl_country_master' : (CountryMaster, CountryMasterSerializer),
	'tbl_class_master' : (ClassMaster, ClassMasterSerializer),
	'tbl_supplier_master' :(SupplierMaster, SupplierMasterSerializer),
	'tbl_opsauthority_master': (OpsAuthorityMaster, OpsAuthorityMasterSerializer),
	'tbl_generic_master': (GenericMaster, GenericMasterSerializer),
	'tbl_establishment_master': (EstablishmentMaster, EstablishmentMasterSerializer),
	'tbl_propulsion_master': (PropulsionMaster, PropulsionMasterSerializer),
	'tbl_manufacturer_master': (ManufacturerMaster, ManufacturerMasterSerializer),
	'tbl_equipment_master': (EquipmentMaster, EquipmentMasterSerializer),
	'tbl_ship_master': (ShipMaster, ShipMasterSerializer),

 	# --- PostgreSQL Views  Remove if not needed ---
	'vw_section_department_details': (VwSectionDepartment, VwSectionDepartmentSerializer),
	'vw_section_group_details': (VwSectionGroupDetails, VwSectionGroupDetailsSerializer),
	'vw_activity_type_details': (VwActivityTypeDetails, VwActivityTypeDetailsSerializer),
	'vw_country_supplier_details': (VwCountrySupplierDetails, VwCountrySupplierDetailsSerializer),
	'vw_command_opsauthority_details': (VwCommandOpsauthorityDetails, VwCommandOpsauthorityDetailsSerializer),
	'vw_command_opsauthority_establishment_details': (VwCommandOpsauthorityEstablishmentDetails, VwCommandOpsauthorityEstablishmentDetailsSerializer),
	'vw_country_manufacturer_details': (VwCountryManufacturerDetails, VwCountryManufacturerDetailsSerializer),
	'vw_section_equipment_group_details': (VwSectionEquipmentGroupDetails, VwSectionEquipmentGroupDetailsSerializer),
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

def crud_list(user, table_name, get_max_id, column_name):
    check_permission(user, table_name, 'view')
    model, serializer_class = ALLOWED_TABLES[table_name]
    # Only return active records if is_active field exists, unless get_max_id is True
    if get_max_id and column_name:
        queryset = model.objects.all()  # Do not filter by is_active
    else:
        if hasattr(model, 'is_active') or 'is_active' in [f.name for f in model._meta.fields]:
            field = model._meta.get_field('is_active')
            if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
                queryset = model.objects.filter(is_active=1)
            else:
                queryset = model.objects.filter(is_active=True)
        else:
            queryset = model.objects.all()
    serializer = serializer_class(queryset, many=True)
    if get_max_id and column_name:
        print(f"Fetching max ID for column '{column_name}' in table '{table_name}'")
        # Validate that the column exists in the model
        try:
            field = model._meta.get_field(column_name)
        except:
            return Response({
                'success': False,
                'message': f'Invalid column name: {column_name}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Fetch max value of the specified column (from all records)
        try:
            max_value = model.objects.aggregate(max_id=models.Max(column_name))['max_id']
            if max_value is None:
                return Response({
                    'success': True,
                    'message': 'No records found to determine max ID.',
                    'data': None
                })
            if isinstance(field, (models.SmallIntegerField, models.IntegerField)):
                next_id = max_value + 1
                formatted_id = f"{next_id:05d}"
            elif isinstance(field, models.CharField):
                prefix = ''.join(filter(str.isalpha, max_value))
                num_part = ''.join(filter(str.isdigit, max_value))
                if num_part:
                    next_num = int(num_part) + 1
                else:
                    next_num = 1
                formatted_id = f"{prefix}-{next_num:05d}"
            else:
                return Response({
                    'success': False,
                    'message': 'Unsupported column type for max ID generation.',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'success': True,
                'message': 'Next ID fetched successfully.',
                'data': {
                    'next_id': formatted_id
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error fetching max ID: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
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

def crud_list_col_values(user, table_name, column_list):
	# Validate table_name
	if not table_name or table_name not in ALLOWED_TABLES:
		return Response({
			'success': False,
			'message': 'Invalid or missing table_name.',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)

	# Validate column_list
	if not column_list or not isinstance(column_list, list) or not all(isinstance(col, str) for col in column_list):
		return Response({
			'success': False,
			'message': 'Invalid or missing column_list. Must be a list of column names.',
			'data': None
		}, status=status.HTTP_400_BAD_REQUEST)

	model, _ = ALLOWED_TABLES[table_name]
	model_fields = [f.name for f in model._meta.get_fields()]
	for col in column_list:
		if col not in model_fields:
			return Response({
				'success': False,
				'message': f'Column "{col}" does not exist in table "{table_name}".',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)

	# Query and process for unique dropdown options
	try:
		if len(column_list) != 2:
			return Response({
				'success': False,
				'message': 'column_list must contain exactly two columns: [id_column, name_column] for dropdown.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)

		id_col, name_col = column_list
		queryset = model.objects.values(id_col, name_col)
		if 'is_active' in model_fields:
			queryset = queryset.filter(is_active=True)
		# Build a mapping: name_col -> first id_col (ignore duplicates)
		name_to_id = {}
		for row in queryset:
			name = row[name_col]
			id_val = row[id_col]
			if name not in name_to_id:
				name_to_id[name] = id_val
		# Prepare response: one entry per unique name_col, with its id, ordered by id_col
		result = [
			{'id': id_val, 'name': name}
			for name, id_val in name_to_id.items()
		]
		result.sort(key=lambda x: x['id'])
		return Response({
			'success': True,
			'message': f'Distinct dropdown options for {name_col} from {table_name}.',
			'data': result
		}, status=status.HTTP_200_OK)
	except Exception as e:
		return Response({
			'success': False,
			'message': f'Error fetching distinct values: {str(e)}',
			'data': None
		}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
		get_max_id = request.data.get('get_max_id', False)  # NEW: flag to get max ID
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
		
		if method_name not in ['create', 'list', 'view', 'update', 'delete', 'list_col_values']:
			return Response({
				'success': False,
				'message': 'Invalid method name. Allowed: create, list, view, update, delete, list_col_values',
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
			return crud_list(request.user, table_name, get_max_id, column_name)
		
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
		
		elif method_name == 'list_col_values':
			column_list = request.data.get('column_list')
			return crud_list_col_values(request.user, table_name, column_list)
		
		else:
			return Response({
				'success': False,
				'message': 'Invalid request.',
				'data': None
			}, status=status.HTTP_400_BAD_REQUEST)




