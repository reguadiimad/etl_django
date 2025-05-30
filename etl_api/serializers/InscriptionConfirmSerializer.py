from rest_framework import serializers
from ..models.inscription import Inscription


class InscriptionConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ['confirmed', 'confirmed_by']
