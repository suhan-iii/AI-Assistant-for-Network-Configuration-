from django.contrib import admin
from .models import NetworkConfig

@admin.register(NetworkConfig)
class NetworkConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'config_type', 'status', 'created_at']
    list_filter = ['status', 'config_type', 'created_at']
    search_fields = ['natural_language_input', 'generated_config']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Input', {
            'fields': ('natural_language_input', 'config_type')
        }),
        ('Output', {
            'fields': ('generated_config', 'status', 'validation_errors')
        }),
        ('Metadata', {
            'fields': ('user', 'file_path', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
