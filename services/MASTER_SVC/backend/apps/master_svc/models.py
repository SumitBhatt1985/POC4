from django.db import models

class CommandMaster(models.Model):
	command = models.CharField(max_length=255)
	hq = models.CharField(max_length=255)
	code = models.CharField(max_length=50)
	class Meta:
		db_table = 'tbl_command_master'

class DepartmentMaster(models.Model):
	name = models.CharField(max_length=255)
	type = models.CharField(max_length=100)
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
	ship_state = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	class Meta:
		db_table = 'tbl_ship_state_master'

class ShipLocationMaster(models.Model):
	ship_location = models.CharField(max_length=255)
	ship_state = models.ForeignKey(ShipStateMaster, on_delete=models.CASCADE, related_name='locations')
	is_active = models.BooleanField(default=True)
	class Meta:
		db_table = 'tbl_ship_location_master'

class ActivityTypeMaster(models.Model):
	ship_activity_type = models.CharField(max_length=255)
	ship_location = models.ForeignKey(ShipLocationMaster, on_delete=models.CASCADE, related_name='activity_types')
	is_active = models.BooleanField(default=True)
	class Meta:
		db_table = 'tbl_activity_type_master'

class ActivityDetailsMaster(models.Model):
	# 'Missing' field not specified, so only activity_type_id and is_active are used
	activity_type = models.ForeignKey(ActivityTypeMaster, on_delete=models.CASCADE, related_name='activity_details')
	is_active = models.BooleanField(default=True)
	class Meta:
		db_table = 'tbl_activity_details_master'

class LubricantMaster(models.Model):
	lubricant_name = models.CharField(max_length=255)
	lubricant_code = models.CharField(max_length=100)
	lubricant_type = models.CharField(max_length=100)
	unit = models.CharField(max_length=50)
	is_active = models.BooleanField(default=True)
	class Meta:
		db_table = 'tbl_lubricant_master'
