from rest_framework import serializers

from ..models import SportMenuItem



class SportMenuSerializer(serializers.ModelSerializer):

	pos_before = serializers.IntegerField(write_only=True, required=False)
	pos_after = serializers.IntegerField(write_only=True, required=False)

	class Meta:
		model = SportMenuItem
		fields = '__all__'
