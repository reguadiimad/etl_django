from rest_framework import serializers
from ..models.admin import Admin, NewsLetterEmails
from rest_framework.validators import UniqueValidator

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin

        fields = '__all__' 
        read_only_fields = ['admin_id']  # Prevents ID from being changed

class NewsLetterEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterEmails
        fields = ['id', 'email']
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=NewsLetterEmails.objects.all())]}
        }
