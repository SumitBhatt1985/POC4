from django.db import models

# Add your SFD models here
from django.db import models

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
    command_id = models.CharField(max_length=255)
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
    removal_date = models.CharField(max_length=50)
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
    decommission_date = models.CharField(max_length=50)
    scheduled_decommission_date = models.CharField(max_length=50)
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
    commission_date = models.CharField(max_length=50)
    decommission = models.CharField(max_length=50)
    is_active = models.SmallIntegerField(default=1)
    class Meta:
        db_table = 'tbl_ship_master'
        
class VwSfdSectionAdd(models.Model):
	section_id = models.CharField(db_column='section_id', max_length=50, primary_key=True)
	section_name = models.CharField(db_column='section_name', max_length=255)
	department_id = models.CharField(db_column='department_id', max_length=50)
	department_name = models.CharField(db_column='department_name', max_length=255)
	is_active = models.SmallIntegerField(db_column='is_active', default=1)

	class Meta:
		managed = False  # No migrations, read-only
		db_table = 'vw_sfd_section_add'



