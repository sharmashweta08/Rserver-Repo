'''Unit Test for Network Service'''
import unittest
from unittest.mock import patch, Mock
from services.network_construct import NetworkService
from config import CdkConfig

class TestNetworkService(unittest.TestCase):
    """Test Network Service class"""
    def setUp(self):
        """Setup Function"""
        self.addCleanup(patch.stopall)
        self.mock_stack=Mock()
        self.mock_vpc=Mock()
        self.mock_alb_securitygroup=Mock()
        self.mock_ec2_security_group=Mock()
        self.mock_create_security_group=patch("aws_cdk.aws_ec2.SecurityGroup", spec=True).start()
        self.mock_peer=patch("aws_cdk.aws_ec2.Peer", spec=True).start()
        self.mock_port=patch("aws_cdk.aws_ec2.Port", spec=True).start()


    def test_create_alb_security_group_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_network_act = NetworkService.create_alb_security_group(self.mock_stack, \
            self.mock_vpc)
        #Assert
        self.mock_create_security_group.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['network_resources']['alb_security_group']['id'],
            vpc=self.mock_vpc,
            allow_all_outbound=True,
            security_group_name=CdkConfig.config['network_resources']\
                ['alb_security_group']['security_group_name']
        )
        self.mock_alb_securitygroup.add_ingress_rule(
            self.mock_peer.any_ipv4(),
            self.mock_port.tcp(80),
            description=CdkConfig.config['network_resources']['alb_security_group']\
                ['description_80']
        )
        self.mock_alb_securitygroup.add_ingress_rule(
            self.mock_peer.any_ipv4(),
            self.mock_port.tcp(443),
            description=CdkConfig.config['network_resources']['alb_security_group']\
                ['description_443']
        )
        test_s3_assert = self.mock_create_security_group.return_value
        self.assertEqual(test_network_act, test_s3_assert)

    def test_create_ec2_security_group_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_ec2_sg_act = NetworkService.create_ec2_security_group(self.mock_stack, \
            self.mock_vpc, self.mock_alb_securitygroup)
        #Assert
        self.mock_create_security_group.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['network_resources']['ec2_security_group']['id'],
            vpc=self.mock_vpc,
            allow_all_outbound=True,
            security_group_name=CdkConfig.config['network_resources']\
                ['ec2_security_group']['security_group_name']
        )
        self.mock_ec2_security_group.add_ingress_rule(
            self.mock_alb_securitygroup,
            self.mock_port.tcp(8787),
            description="Allow ALB to EC2"
        )
        test_ec2_sg_assert = self.mock_create_security_group.return_value
        self.assertEqual(test_ec2_sg_act, test_ec2_sg_assert)
