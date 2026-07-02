from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import NetworkConfig
from .serializers import NetworkConfigSerializer, ConfigGenerationSerializer
from .services import ConfigParser, ConfigValidator

class ConfigViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkConfigSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return NetworkConfig.objects.all()
    
    @action(detail=False, methods=['post'], serializer_class=ConfigGenerationSerializer)
    def generate(self, request):
        """
        Generate network configuration from natural language input
        Endpoint: POST /api/configs/generate/
        """
        serializer = ConfigGenerationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        command = serializer.validated_data['command']
        use_nlp = serializer.validated_data.get('use_nlp', False)
        
        try:
            # Parse the command
            parser = ConfigParser(use_nlp=use_nlp)
            generated_config, config_type = parser.parse_instruction(command)
            
            # Validate the generated config
            validator = ConfigValidator()
            validation_result = validator.validate(generated_config, config_type)
            
            # Create and save the config
            config = NetworkConfig.objects.create(
                user=request.user if request.user.is_authenticated else None,
                natural_language_input=command,
                generated_config=generated_config,
                config_type=config_type,
                status='validated' if validation_result['is_valid'] else 'error',
                validation_errors=validation_result.get('errors', {})
            )
            
            return Response({
                'id': config.id,
                'config': generated_config,
                'config_type': config_type,
                'status': config.status,
                'validation_errors': config.validation_errors,
                'is_valid': validation_result['is_valid']
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        """
        Export config as .cfg file
        Endpoint: POST /api/configs/{id}/export/
        """
        config = self.get_object()
        return Response({'file_path': f'/configs/{config.id}.cfg'})
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """
        Apply config in mock network environment
        Endpoint: POST /api/configs/{id}/apply/
        """
        config = self.get_object()
        config.status = 'applied'
        config.save()
        return Response({'status': 'Config applied successfully'})
