# Serializer for PostgreSQL view vw_activity_type_details
from rest_framework import serializers
from .models import VwActivityTypeDetails
from .models import VwCountrySupplierDetails, VwCommandOpsauthorityDetails, VwCommandOpsauthorityEstablishmentDetails, VwCountryManufacturerDetails, VwSectionEquipmentGroupDetails
from .models import ShipStateMaster, ShipLocationMaster, ActivityTypeMaster, ActivityDetailsMaster, LubricantMaster

from .models import CommandMaster, DepartmentMaster, EquipmentCategoryMaster, ShipCategoryMaster, RoleMaster
from .models import (SectionMaster, GroupMaster, CountryMaster, ClassMaster, SupplierMaster, OpsAuthorityMaster,
					GenericMaster, EstablishmentMaster, PropulsionMaster, ManufacturerMaster, EquipmentMaster, 
                    ShipMaster)

from .models import VwSectionGroupDetails, VwSectionDepartment

class VwActivityTypeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwActivityTypeDetails
        fields = ['activity_type_id', 'activity_type', 'activity_id', 'activity_detail', 'is_active']

# Serializer for PostgreSQL view vw_sfd_section_add
class VwCountrySupplierDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwCountrySupplierDetails
        fields = ['country_name', 'supplier_id', 'supplier_name', 'address', 'city', 'state', 'contanct_number', 'email']

# Serializer for PostgreSQL view vw_command_opsauthority_details
class VwCommandOpsauthorityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwCommandOpsauthorityDetails
        fields = ['opsauthority_id', 'ops_authority', 'command_id', 'command', 'address', 'is_active']  

# Serializer for PostgreSQL view vw_command_opsauthority_establishment_details
class VwCommandOpsauthorityEstablishmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwCommandOpsauthorityEstablishmentDetails
        fields = ['establishment_name', 'command', 'ops_authority', 'establishment_category']

# Serializer for PostgreSQL view vw_country_manufacturer_details
class VwCountryManufacturerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwCountryManufacturerDetails
        fields = ['country_name', 'manufacturer_id', 'manufacturer_name', 'address', 'city', 'state', 'contact_number', 'email']

# Serializer for PostgreSQL view vw_section_equipment_group_details
class VwSectionEquipmentGroupDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSectionEquipmentGroupDetails
        fields = ['section_id', 'section_name', 'equipment_id', 'equipment_model', 'group_id', 'group_name', 'category_id', 'equipment_type', 'equipment_name', 'location_on_board', 'maintop_number', 'authority', 'total_fits', 'is_active']

# Serializer for PostgreSQL view vw_section_group_details

class VwSectionDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSectionDepartment
        fields = ['section_id', 'name', 'department_id', 'department_name', 'is_active']
        
class VwSectionGroupDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSectionGroupDetails
        fields = ['section_name', 'group_id', 'group_name']

# master serializers
class CommandMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommandMaster
		fields = '__all__'

class DepartmentMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepartmentMaster
		fields = ['department_id', 'name', 'ship_id', 'type', 'status', 'is_active']

class EquipmentCategoryMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = EquipmentCategoryMaster
		fields = '__all__'

class ShipCategoryMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShipCategoryMaster
		fields = '__all__'

class RoleMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = RoleMaster
		fields = '__all__'
  
class ShipStateMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShipStateMaster
		fields = '__all__'

class ShipLocationMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShipLocationMaster
		fields = '__all__'

class ActivityTypeMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ActivityTypeMaster
		fields = '__all__'

class ActivityDetailsMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = ActivityDetailsMaster
		fields = '__all__'

class LubricantMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = LubricantMaster
		fields = '__all__'

# --- SFD Master Serializers ---

class SectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionMaster
        fields = ['section_id', 'name', 'department_id', 'is_active']

class GroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMaster
        fields = ['group_id', 'name', 'section_id', 'generic_id', 'is_active']

class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMaster
        fields = ['country_id', 'name', 'iso_code', 'is_active']

class ClassMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMaster
        fields = ['class_id', 'name', 'type', 'is_active']

class SupplierMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierMaster
        fields = [
            'supplier_id', 'name', 'address', 'contact_number', 'code',
            'contact_person', 'email', 'city', 'area', 'country_id', 'state',
            'equipment_supplied', 'is_active'
        ]

class OpsAuthorityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsAuthorityMaster
        fields = ['opsauthority_id', 'ops_authority', 'command_id', 'address', 'is_active']

class GenericMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMaster
        fields = ['generic_id', 'name', 'description', 'is_active']

class EstablishmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentMaster
        fields = [
            'establishment_id', 'name', 'command', 'opsauthority_id',
            'category_id', 'category_name', 'is_active'
        ]

class PropulsionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropulsionMaster
        fields = ['propulsion_id', 'name', 'category', 'is_active']

class ManufacturerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerMaster
        fields = [
            'manufacturer_id', 'name', 'address', 'contact_number', 'code',
            'contact_person', 'email', 'city', 'area', 'country_id', 'state',
            'equipment_manufactured', 'is_active'
        ]

class EquipmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMaster
        fields = [
            'equipment_id', 'equipment_name', 'generic_id', 'category_id',
            'section_id', 'group_id', 'equipment_serial_no', 'equipment_code',
            'equipment_model', 'maintop_number', 'acquiant_issued', 'authority',
            'ilms_equipment_code', 'total_fits', 'ship_applicable',
            'location_on_board', 'equipment_type', 'ship_id', 'removal_date',
            'description', 'srar_equipment', 'system', 'sub_system', 'assembly',
            'department_id', 'obsolete', 'is_active'
        ]

class ShipMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipMaster
        fields = [
            'ship_id', 'name', 'command_id', 'pennant_no', 'ship_category_id',
            'class_id', 'displacement', 'base_port', 'ship_builder',
            'decommission_date', 'scheduled_decommission_date', 'propulsion_id',
            'refit_authority', 'signal_name', 'address', 'contact_number',
            'nud_mail', 'nic_mail', 'sdrsref', 'overseeing_team', 'remark',
            'yard_no', 'classification_society', 'reference_no',
            'length_between_perpendiculars', 'length_overall',
            'wetted_surface_area_underwater', 'module_breadth',
            'standard_discplacement', 'wetted_surface_area_boottop',
            'standard_draft', 'full_load_displacement', 'depth_of_main_deck',
            'full_load_draft', 'max_continuous_speed', 'engine_each_rating',
            'endurance_in_days', 'economic_speed', 'opsauthority_id', 'port_id',
            'origin', 'commission_date', 'decommission', 'is_active'
        ]







