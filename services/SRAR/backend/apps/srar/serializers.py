# --- New Master Serializers ---
from .models import ShipStateMaster, ShipLocationMaster, ActivityTypeMaster, ActivityDetailsMaster, LubricantMaster
from rest_framework import serializers
  
# --- SRAR Master Serializers ---
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

