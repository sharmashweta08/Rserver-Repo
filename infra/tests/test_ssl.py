'''Unit Test for SSL Service'''
import unittest
from unittest.mock import patch, Mock
from services.ssl_construct import SSLService
from config import CdkConfig

class TestSslService(unittest.TestCase):
    """Test SSL Service class"""
    def setUp(self):
        """Setup Function"""
        self.addCleanup(patch.stopall)
        self.mock_stack=Mock()
        self.mock_rserver_hosted_zone=Mock()
        self.mock_certificate=patch("aws_cdk.aws_certificatemanager.Certificate", spec=True).start()
        self.mock_certificate_validation=patch\
            ("aws_cdk.aws_certificatemanager.CertificateValidation", spec=True).start()
        self.mock_core_tags=patch("aws_cdk.core.Tags", spec=True).start()

    def test_create_ssl_expected_parameters(self):
        """Create SSL Function"""
        #Act
        test_alb_act = SSLService.create_ssl(self.mock_stack, self.mock_rserver_hosted_zone)
        #Assert
        certificate = self.mock_certificate.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['ssl_resources']['id'],
            domain_name=CdkConfig.config['ssl_resources']['domain_name'],
            validation=self.mock_certificate_validation.from_dns(
                hosted_zone=self.mock_rserver_hosted_zone
            )
        )
        self.mock_core_tags.of(certificate).add(
            key=CdkConfig.config['ssl_resources']['tag_key'],
            value=CdkConfig.config['ssl_resources']['tag_value']
        )
        test_alb_assert = self.mock_certificate.return_value
        self.assertEqual(test_alb_act, test_alb_assert)
