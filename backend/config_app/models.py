from django.db import models
from django.contrib.auth.models import User

class NetworkConfig(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('applied', 'Applied'),
        ('error', 'Error'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='configs', null=True, blank=True)
    natural_language_input = models.TextField()
    generated_config = models.TextField()
    config_type = models.CharField(max_length=50, default='vlan')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    validation_errors = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.config_type.upper()} - {self.created_at}"
