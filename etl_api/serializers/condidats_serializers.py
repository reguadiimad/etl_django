from rest_framework import serializers
from ..models.condidats import Condidats

class CondidatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condidats
        fields = '__all__'
