
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
