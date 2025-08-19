
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
