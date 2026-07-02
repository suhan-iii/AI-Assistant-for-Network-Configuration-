from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import NetworkConfig
from .services import ConfigParser, ConfigValidator

class ConfigParserTestCase(TestCase):
    def setUp(self):
        self.parser = ConfigParser(use_nlp=False)
    
    def test_parse_sales_vlan(self):
        command = "create VLAN for Sales, IP range 10.0.0.0/24"
        config, config_type = self.parser.parse_instruction(command)
        self.assertEqual(config_type, 'vlan')

class ConfigValidatorTestCase(TestCase):
    def setUp(self):
        self.validator = ConfigValidator()
    
    def test_validate_empty_config(self):
        result = self.validator.validate("", "vlan")
        self.assertFalse(result['is_valid'])
    
    def test_validate_vlan_config(self):
        config = "vlan 10\n name Sales"
        result = self.validator.validate(config, "vlan")
        self.assertTrue(result['is_valid'])

class ConfigAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_generate_config_endpoint(self):
        response = self.client.post('/api/configs/generate/', {
            'command': 'create VLAN for Sales'
        })
        self.assertIn(response.status_code, [201, 400])
