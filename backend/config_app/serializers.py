from rest_framework import serializers
from .models import NetworkConfig

class NetworkConfigSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True, allow_null=True)
    
    class Meta:
        model = NetworkConfig
        fields = ['id', 'user', 'user_username', 'natural_language_input', 'generated_config', 
                  'config_type', 'status', 'validation_errors', 'created_at', 'updated_at', 'file_path']
        read_only_fields = ['id', 'user', 'status', 'validation_errors', 'created_at', 'updated_at']

class ConfigGenerationSerializer(serializers.Serializer):
    command = serializers.CharField(max_length=500)
    use_nlp = serializers.BooleanField(default=False, required=False)
