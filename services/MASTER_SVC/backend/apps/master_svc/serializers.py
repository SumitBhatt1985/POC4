# --- New Master Serializers ---
from .models import ShipStateMaster, ShipLocationMaster, ActivityTypeMaster, ActivityDetailsMaster, LubricantMaster
from rest_framework import serializers
from .models import CommandMaster, DepartmentMaster, EquipmentCategoryMaster, ShipCategoryMaster, RoleMaster

class CommandMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommandMaster
		fields = '__all__'

class DepartmentMasterSerializer(serializers.ModelSerializer):
	class Meta:
		model = DepartmentMaster
		fields = '__all__'

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

