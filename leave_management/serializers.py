from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
    
    def validate_days_taken(self, value):
        if value <= 0:
            raise serializers.ValidationError("Days taken must be positive.")
        return value