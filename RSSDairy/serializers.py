from rest_framework import serializers
from .models import RfidScan

class RfidScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RfidScan
        fields = "__all__"
