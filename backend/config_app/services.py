import os
from typing import Tuple, Dict, Any

class ConfigParser:
    """
    Parse natural language input and generate network configuration
    Can use regex-based (MVP) or NLP-based (OpenAI/HuggingFace)
    """
    
    def __init__(self, use_nlp=False):
        self.use_nlp = use_nlp
        self.config_templates = {
            'sales': 'configs/vlan_sales.cfg',
            'hr': 'configs/vlan_hr.cfg',
            'firewall': 'configs/firewall_main.cfg',
        }
    
    def parse_instruction(self, command: str) -> Tuple[str, str]:
        """
        Parse natural language command and return generated config and type
        Returns: (generated_config, config_type)
        """
        command_lower = command.lower()
        
        # MVP: Simple regex-based parsing
        if not self.use_nlp:
            return self._parse_regex(command_lower)
        
        # Advanced: NLP-based parsing (TODO)
        else:
            return self._parse_nlp(command)
    
    def _parse_regex(self, command: str) -> Tuple[str, str]:
        """
        Simple regex-based parsing logic
        """
        if 'sales' in command:
            config = self._read_template('sales')
            return config, 'vlan'
        elif 'hr' in command:
            config = self._read_template('hr')
            return config, 'vlan'
        elif 'firewall' in command:
            config = self._read_template('firewall')
            return config, 'firewall'
        else:
            raise ValueError(f"Command not recognized: {command}")
    
    def _parse_nlp(self, command: str) -> Tuple[str, str]:
        """
        NLP-based parsing using OpenAI or HuggingFace
        TODO: Implement OpenAI integration
        """
        raise NotImplementedError("NLP parsing not yet implemented")
    
    def _read_template(self, config_type: str) -> str:
        """
        Read config template from file
        """
        template_path = self.config_templates.get(config_type)
        if template_path and os.path.exists(template_path):
            with open(template_path, 'r') as f:
                return f.read()
        raise FileNotFoundError(f"Template not found: {config_type}")


class ConfigValidator:
    """
    Validate generated network configuration
    """
    
    def validate(self, config: str, config_type: str) -> Dict[str, Any]:
        """
        Validate configuration syntax and structure
        Returns: {'is_valid': bool, 'errors': dict}
        """
        errors = {}
        
        # Basic validation
        if not config or len(config.strip()) == 0:
            errors['config'] = 'Configuration is empty'
            return {'is_valid': False, 'errors': errors}
        
        # Type-specific validation
        if config_type == 'vlan':
            errors.update(self._validate_vlan(config))
        elif config_type == 'firewall':
            errors.update(self._validate_firewall(config))
        
        return {'is_valid': len(errors) == 0, 'errors': errors}
    
    def _validate_vlan(self, config: str) -> Dict[str, str]:
        """
        Validate VLAN configuration
        """
        errors = {}
        
        if 'vlan' not in config.lower():
            errors['vlan'] = 'VLAN configuration missing vlan keyword'
        
        return errors
    
    def _validate_firewall(self, config: str) -> Dict[str, str]:
        """
        Validate firewall configuration
        """
        errors = {}
        
        if 'access-list' not in config.lower():
            errors['firewall'] = 'Firewall configuration missing access-list keyword'
        
        return errors
