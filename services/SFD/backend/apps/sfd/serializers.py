# --- SFD Master Serializers ---
# --- New Master Serializers ---
from rest_framework import serializers
from .models import (SectionMaster, GroupMaster, CountryMaster, ClassMaster, SupplierMaster, OpsAuthorityMaster,
					GenericMaster, EstablishmentMaster, PropulsionMaster, ManufacturerMaster, EquipmentMaster, 
                    ShipMaster, VwSfdSectionAdd, sfdShipEquipmentDetails, VwSfdAttachRefernce, VwShipClass,
                    VwSfdEquipmentShipDetails)

class SectionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionMaster
        fields = ['section_id', 'name', 'department_id']

class GroupMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMaster
        fields = ['group_id', 'name', 'section_id', 'generic_id']

class CountryMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMaster
        fields = ['country_id', 'name', 'iso_code']

class ClassMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassMaster
        fields = ['class_id', 'name', 'type']

class SupplierMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierMaster
        fields = [
            'supplier_id', 'name', 'address', 'contact_number', 'code',
            'contact_person', 'email', 'city', 'area', 'country_id', 'state',
            'equipment_supplied'
        ]

class OpsAuthorityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpsAuthorityMaster
        fields = ['opsauthority_id', 'ops_authority', 'command_id', 'address']

class GenericMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericMaster
        fields = ['generic_id', 'name', 'description']

class EstablishmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstablishmentMaster
        fields = [
            'establishment_id', 'name', 'command', 'opsauthority_id',
            'category_id', 'category_name'
        ]

class PropulsionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropulsionMaster
        fields = ['propulsion_id', 'name', 'category']

class ManufacturerMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerMaster
        fields = [
            'manufacturer_id', 'name', 'address', 'contact_number', 'code',
            'contact_person', 'email', 'city', 'area', 'country_id', 'state',
            'equipment_manufactured'
        ]

class EquipmentMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentMaster
        fields = [
            'equipment_id', 'equipment_name', 'category_id',
            'section_id', 'group_id', 'equipment_serial_no', 'equipment_code',
            'equipment_model', 'maintop_number', 'acquiant_issued', 'authority',
            'ilms_equipment_code', 'total_fits', 'ship_applicable',
            'location_on_board', 'equipment_type', 'ship_id', 'removal_date',
            'description', 'srar_equipment', 'system', 'sub_system', 'assembly',
            'obsolete', 'manufacturer_id'
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
            'origin', 'commission_date', 'decommission'
        ]
        
# Serializer for PostgreSQL view vw_sfd_section_add
class VwSfdSectionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSfdSectionAdd
        fields = ['section_id', 'section_name', 'department_id', 'department_name', 'is_active']

class VwSfdAttachRefernceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSfdAttachRefernce
        fields = ['section_name', 'section_id', 'class_name', 'class_id', 'sfd_ship_name', 'sfd_ship_id']

class VwShipClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwShipClass
        fields = ['class_name', 'class_id', 'ship_name', 'ship_id']

class sfdShipEquipmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = sfdShipEquipmentDetails
        fields = '__all__'

class VwSfdEquipmentShipDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VwSfdEquipmentShipDetails
        fields = ['ship_name', 'location_code', 'location_on_board', 'equipment_serial_no', 'no_of_fits']


