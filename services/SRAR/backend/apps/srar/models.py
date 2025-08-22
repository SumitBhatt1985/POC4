from django.db import models
  
  
# --- SRAR Master Tables ---
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

