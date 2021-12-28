'''Unit Test for ALB Service'''
import unittest
from unittest.mock import patch, Mock
from services.hosted_zone_construct import HostedZoneService
from config import CdkConfig

class TestAlbService(unittest.TestCase):
    """Test ALB Service class"""
    def setUp(self):
        """Setup Function"""
        self.addCleanup(patch.stopall)
        self.mock_stack=Mock()
        self.mock_alb=Mock()
        self.mock_rserver_hosted_zone=Mock()
        self.mock_hosted_zone=patch("aws_cdk.aws_route53.HostedZone", spec=True).start()
        self.mock_a_record=patch("aws_cdk.aws_route53.ARecord",spec=True).start()
        self.mock_record_path=patch("aws_cdk.aws_route53.RecordTarget",spec=True).start()
        self.mock_targets=patch("aws_cdk.aws_route53_targets.LoadBalancerTarget",spec=True).start()

    def test_create_hosted_zone_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_hosted_zone_act = HostedZoneService.create_hosted_zone(self.mock_stack)
        #Assert
        self.mock_hosted_zone.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['hosted_zone_resources']['rserver_hosted_zone']['id'],
            zone_name=CdkConfig.config['hosted_zone_resources']['rserver_hosted_zone']['zone_name']
        )
        test_hosted_zone_assert = self.mock_hosted_zone.return_value
        self.assertEqual(test_hosted_zone_act, test_hosted_zone_assert)

    def test_create_a_record_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_a_record_act = HostedZoneService.create_a_record(self.mock_stack, self.mock_alb, \
            self.mock_rserver_hosted_zone)
        #Assert
        self.mock_a_record.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['hosted_zone_resources']['a_record']['id'],
            target=self.mock_record_path.from_alias(
                self.mock_targets(self.mock_alb)
            ),
            zone=self.mock_rserver_hosted_zone
        )
        test_a_record_assert = self.mock_a_record.return_value
        self.assertEqual(test_a_record_act, test_a_record_assert)
