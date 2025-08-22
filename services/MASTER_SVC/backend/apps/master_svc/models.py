# Model for PostgreSQL view vw_activity_type_details
from django.db import models

class VwActivityTypeDetails(models.Model):
    activity_type_id = models.CharField(db_column='activity_type_id', max_length=10)
    activity_type = models.CharField(db_column='activity_type', max_length=50)
    activity_id = models.CharField(db_column='activity_id', max_length=10, primary_key=True)
    activity_detail = models.CharField(db_column='activity_detail', max_length=100)
    is_active = models.SmallIntegerField(db_column='is_active', default=True)	

    class Meta:
        managed = False
        db_table = 'vw_activity_type_details'

# Model for PostgreSQL view vw_country_supplier_details
class VwCountrySupplierDetails(models.Model):
    country_name = models.CharField(db_column='country_name', max_length=200)
    supplier_id = models.CharField(db_column='supplier_id', max_length=10, primary_key=True)
    supplier_name = models.CharField(db_column='supplier_name', max_length=50)
    address = models.CharField(db_column='address', max_length=50)
    city = models.CharField(db_column='city', max_length=50)
    state = models.CharField(db_column='state', max_length=50)
    contanct_number = models.CharField(db_column='contanct_number', max_length=50)
    email = models.CharField(db_column='email', max_length=50)

    class Meta:
        managed = False
        db_table = 'vw_country_supplier_details'

# Model for PostgreSQL view vw_command_opsauthority_details
class VwCommandOpsauthorityDetails(models.Model):
    opsauthority_id = models.CharField(db_column='opsauthority_id', max_length=10, primary_key=True)	
    ops_authority = models.CharField(db_column='ops_authority', max_length=100)
    command_id = models.CharField(db_column='command_id', max_length=10)
    command = models.CharField(db_column='command', max_length=50)
    address = models.CharField(db_column='address', max_length=200)
    is_active = models.SmallIntegerField(db_column='is_active', default=True)

    class Meta:
        managed = False
        db_table = 'vw_command_opsauthority_details'

# Model for PostgreSQL view vw_command_opsauthority_establishment_details
class VwCommandOpsauthorityEstablishmentDetails(models.Model):
    establishment_name = models.CharField(db_column='establishment_name', max_length=50)
    command = models.CharField(db_column='command', max_length=50)
    ops_authority = models.CharField(db_column='ops_authority', max_length=100)
    establishment_category = models.CharField(db_column='establishment_category', max_length=100)

    class Meta:
        managed = False
        db_table = 'vw_command_opsauthority_establishment_details'

# Model for PostgreSQL view vw_country_manufacturer_details
class VwCountryManufacturerDetails(models.Model):
    country_name = models.CharField(db_column='country_name', max_length=200)
    manufacturer_id = models.CharField(db_column='manufacturer_id', max_length=10, primary_key=True)
    manufacturer_name = models.CharField(db_column='manufacturer_name', max_length=50)
    address = models.CharField(db_column='address', max_length=100)
    city = models.CharField(db_column='city', max_length=50)
    state = models.CharField(db_column='state', max_length=50)
    contact_number = models.CharField(db_column='contact_number', max_length=50)
    email = models.CharField(db_column='email', max_length=100)

    class Meta:
        managed = False
        db_table = 'vw_country_manufacturer_details'

# Model for PostgreSQL view vw_section_equipment_group_details
class VwSectionEquipmentGroupDetails(models.Model):
    section_id = models.CharField(db_column='section_id', max_length=10)
    section_name = models.CharField(db_column='section_name', max_length=50)
    equipment_id = models.CharField(db_column='equipment_id', max_length=10, primary_key=True)
    equipment_model = models.CharField(db_column='equipment_model', max_length=50)
    group_id = models.CharField(db_column='group_id', max_length=10)
    group_name = models.CharField(db_column='group_name', max_length=50)
    category_id = models.CharField(db_column='category_id', max_length=10)
    equipment_type = models.CharField(db_column='equipment_type', max_length=100)
    equipment_name = models.CharField(db_column='equipment_name', max_length=50)
    location_on_board = models.CharField(db_column='location_on_board', max_length=100)
    maintop_number = models.CharField(db_column='maintop_number', max_length=50)
    authority = models.CharField(db_column='authority', max_length=50)
    total_fits = models.IntegerField(db_column='total_fits')
    is_active = models.SmallIntegerField(db_column='is_active', default=True)

    class Meta:
        managed = False
        db_table = 'vw_section_equipment_group_details'

# Model for PostgreSQL view vw_sfd_section_add
class VwSectionDepartment(models.Model):
	section_id = models.CharField(db_column='section_id', max_length=10, primary_key=True)
	section_name = models.CharField(db_column='section_name', max_length=5)
	department_id = models.CharField(db_column='department_id', max_length=10)
	department_name = models.CharField(db_column='department_name', max_length=50)
	# is_active = models.BooleanField(db_column='is_active')

	class Meta:
		managed = False  # No migrations, read-only
		db_table = 'vw_section_department_details'
  
class VwSectionGroupDetails(models.Model):
    section_name = models.CharField(db_column='section_name', max_length=50)
    group_id = models.CharField(db_column='group_id', max_length=10, primary_key=True)
    group_name = models.CharField(db_column='group_name', max_length=50)

    class Meta:
        managed = False  # No migrations, read-only
        db_table = 'vw_section_group_details'

class CommandMaster(models.Model):
	command_id = models.CharField(max_length=10)
	command = models.CharField(max_length=255)
	hq = models.CharField(max_length=255)
	code = models.CharField(max_length=50)
	is_active = models.SmallIntegerField(default=1)
	class Meta:
		db_table = 'tbl_command_master'

class DepartmentMaster(models.Model):
    department_id = models.CharField(max_length=10)
    name = models.CharField(max_length=50) 
    ship_id = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    status = models.SmallIntegerField()
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_department_master'

class EquipmentCategoryMaster(models.Model):
	name = models.CharField(max_length=255)
	class Meta:
		db_table = 'tbl_equipment_category_master'

class ShipCategoryMaster(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	class Meta:
		db_table = 'tbl_ship_category_master'

class RoleMaster(models.Model):
	status = models.IntegerField()
	level = models.CharField(max_length=50)
	role_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	class Meta:
		db_table = 'tbl_role_master'
  
  
# --- New Master Tables ---
class ShipStateMaster(models.Model):
	ship_state_id = models.CharField(max_length=100)
	ship_state = models.CharField(max_length=255)
	ship_id = models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.SmallIntegerField(default=True)
	class Meta:
		db_table = 'tbl_ship_state_master'

class ShipLocationMaster(models.Model):
	ship_location_id = models.CharField(max_length=100)
	ship_location = models.CharField(max_length=255)
	ship_state_id = models.CharField(max_length=100, null=True, blank=True)
	ship_id = models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.SmallIntegerField(default=True)
	class Meta:
		db_table = 'tbl_ship_location_master'

class ActivityTypeMaster(models.Model):
	activity_type_id = models.CharField(max_length=255)
	activity_type = models.CharField(max_length=255)
	ship_location_id = models.ForeignKey(ShipLocationMaster, on_delete=models.CASCADE, related_name='activity_types')
	remark = models.CharField(max_length=255, null=True, blank=True)
	status = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.SmallIntegerField(default=True)
	class Meta:
		db_table = 'tbl_activity_type_master'

class ActivityDetailsMaster(models.Model):
	# 'Missing' field not specified, so only activity_type_id and is_active are used
	activity_id = models.CharField(max_length=100)
	activity_type_id = models.CharField(max_length=100)
	activity_detail = models.CharField(max_length=255)
	department_id = models.CharField(max_length=100)
	status = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.SmallIntegerField(default=True)
	class Meta:
		db_table = 'tbl_activity_details_master'

class LubricantMaster(models.Model):
	lubricant_id = models.CharField(max_length=100)
	lubricant_name = models.CharField(max_length=255)
	lubricant_code = models.CharField(max_length=100)
	lubricant_type = models.CharField(max_length=100)
	unit = models.CharField(max_length=50)
	ship_id = models.CharField(max_length=100, null=True, blank=True)
	application = models.CharField(max_length=255)
	specification = models.CharField(max_length=255)
	status = models.CharField(max_length=50, null=True, blank=True)
	is_active = models.SmallIntegerField(default=True)
	class Meta:
		db_table = 'tbl_lubricant_master'

# --- SFD Master Tables ---

class SectionMaster(models.Model):
    section_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    department_id = models.CharField(max_length=50)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_section_master'

class GroupMaster(models.Model):
    group_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    section_id = models.CharField(max_length=50)
    generic_id = models.CharField(max_length=50)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_group_master'

class CountryMaster(models.Model):
    country_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=10)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_country_master'

class ClassMaster(models.Model):
    class_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_class_master'

class SupplierMaster(models.Model):
    supplier_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    country_id = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    equipment_supplied = models.CharField(max_length=255)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_supplier_master'

class OpsAuthorityMaster(models.Model):
    opsauthority_id = models.CharField(max_length=50)
    ops_authority = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_opsauthority_master'

class GenericMaster(models.Model):
    generic_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_generic_master'

class EstablishmentMaster(models.Model):
    establishment_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    command = models.CharField(max_length=255)
    opsauthority_id = models.CharField(max_length=50)
    category_id = models.CharField(max_length=50)
    category_name = models.CharField(max_length=255)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_establishment_master'

class PropulsionMaster(models.Model):
    propulsion_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_propulsion_master'

class ManufacturerMaster(models.Model):
    manufacturer_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    country_id = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    equipment_manufactured = models.CharField(max_length=255)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_manufacturer_master'

class EquipmentMaster(models.Model):
    equipment_id = models.CharField(max_length=50)
    equipment_name = models.CharField(max_length=255)
    generic_id = models.CharField(max_length=50)
    category_id = models.CharField(max_length=50)
    section_id = models.CharField(max_length=50)
    group_id = models.CharField(max_length=50)
    equipment_serial_no = models.CharField(max_length=100)
    equipment_code = models.CharField(max_length=100)
    equipment_model = models.CharField(max_length=100)
    maintop_number = models.CharField(max_length=100)
    acquiant_issued = models.CharField(max_length=100)
    authority = models.CharField(max_length=100)
    ilms_equipment_code = models.CharField(max_length=100)
    total_fits = models.CharField(max_length=100)
    ship_applicable = models.CharField(max_length=100)
    location_on_board = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    ship_id = models.CharField(max_length=50)
    removal_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    srar_equipment = models.CharField(max_length=100)
    system = models.CharField(max_length=100)
    sub_system = models.CharField(max_length=100)
    assembly = models.CharField(max_length=100)
    department_id = models.CharField(max_length=50)
    obsolete = models.CharField(max_length=10)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_equipment_master'

class ShipMaster(models.Model):
    ship_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    command_id = models.CharField(max_length=50)
    pennant_no = models.CharField(max_length=50)
    ship_category_id = models.CharField(max_length=50)
    class_id = models.CharField(max_length=50)
    displacement = models.CharField(max_length=100)
    base_port = models.CharField(max_length=100)
    ship_builder = models.CharField(max_length=255)
    decommission_date = models.DateField(null=True, blank=True)
    scheduled_decommission_date = models.DateField(null=True, blank=True)
    propulsion_id = models.CharField(max_length=50)
    refit_authority = models.CharField(max_length=100)
    signal_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    nud_mail = models.CharField(max_length=100)
    nic_mail = models.CharField(max_length=100)
    sdrsref = models.CharField(max_length=100)
    overseeing_team = models.CharField(max_length=100)
    remark = models.TextField()
    yard_no = models.CharField(max_length=50)
    classification_society = models.CharField(max_length=100)
    reference_no = models.CharField(max_length=100)
    length_between_perpendiculars = models.CharField(max_length=50)
    length_overall = models.CharField(max_length=50)
    wetted_surface_area_underwater = models.CharField(max_length=50)
    module_breadth = models.CharField(max_length=50)
    standard_discplacement = models.CharField(max_length=50)
    wetted_surface_area_boottop = models.CharField(max_length=50)
    standard_draft = models.CharField(max_length=50)
    full_load_displacement = models.CharField(max_length=50)
    depth_of_main_deck = models.CharField(max_length=50)
    full_load_draft = models.CharField(max_length=50)
    max_continuous_speed = models.CharField(max_length=50)
    engine_each_rating = models.CharField(max_length=50)
    endurance_in_days = models.CharField(max_length=50)
    economic_speed = models.CharField(max_length=50)
    opsauthority_id = models.CharField(max_length=50)
    port_id = models.CharField(max_length=50)
    origin = models.CharField(max_length=100)
    commission_date = models.DateField(null=True, blank=True)
    decommission = models.CharField(max_length=50)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_ship_master'





