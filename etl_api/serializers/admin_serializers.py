from rest_framework import serializers
from ..models.admin import Admin

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin

        fields = '__all__' 
        read_only_fields = ['admin_id']  # Prevents ID from being changed
