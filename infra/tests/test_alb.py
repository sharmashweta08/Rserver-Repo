'''Unit Test for ALB Service'''
import unittest
from unittest.mock import patch, Mock
from services.alb_construct import AlbService
from config import CdkConfig

class TestAlbService(unittest.TestCase):               #pylint: disable=too-many-instance-attributes
    """Test ALB Service class"""
    def setUp(self):
        """Setup Function"""
        self.addCleanup(patch.stopall)
        self.mock_stack=Mock()
        self.mock_vpc=None
        self.mock_ec2server=Mock()
        self.mock_public_subnet=Mock()
        self.mock_alb_security_group=Mock()
        self.mock_target_group=Mock()
        self.mock_application_target_group=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup", spec=True).start()
        self.mock_target_type=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.TargetType", spec=True).start()
        self.mock_application_protocol=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol", spec=True).start()
        self.mock_application_protocol_version=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocolVersion", spec=True).start()
        self.mock_instance_id_target=patch\
            ("aws_cdk.aws_elasticloadbalancingv2_targets.InstanceIdTarget", spec=True).start()
        self.mock_application_load_balancer=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer", spec=True).start()
        self.mock_listener_action_redirect=patch\
            ("aws_cdk.aws_elasticloadbalancingv2.ListenerAction.redirect").start()


    def test_create_alb_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_alb_act = AlbService.create_alb(self.mock_stack, self.mock_vpc, self.mock_ec2server, \
            self.mock_public_subnet, self.mock_alb_security_group)
        #Assert
        targetgroup = self.mock_application_target_group.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['alb_resources']['targetgroup']['id'],
            target_type=self.mock_target_type.INSTANCE,
            target_group_name=CdkConfig.config['alb_resources']['targetgroup']\
                ['target_group_name'],
            vpc=self.mock_vpc,
            protocol=self.mock_application_protocol.HTTP,
            port=CdkConfig.config['alb_resources']['targetgroup']['port'],
            protocol_version=self.mock_application_protocol_version.HTTP1,
            health_check={

                "enabled" : True,
                "port" : "8787",
                "path" : "/auth-sign-in"
            }
        )
        self.mock_target_group.add_target(
            self.mock_instance_id_target(self.mock_ec2server.instance_id)
        )
        alb = self.mock_application_load_balancer(
            scope=self.mock_stack,
            id=CdkConfig.config['alb_resources']['alb']['id'],
            load_balancer_name=CdkConfig.config['alb_resources']['alb']['load_balancer_name'],
            internet_facing=True,
            vpc=self.mock_vpc,
            vpc_subnets=self.mock_public_subnet,
            security_group=self.mock_alb_security_group
        )
        alb.add_listener(
            id=CdkConfig.config['alb_resources']['listeners']['id_80'],
            port=80,
            open=False,
            # default_target_groups=[targetgroup]
            default_action=self.mock_listener_action_redirect(
                host="#{host}",
                path="/#{path}",
                port="443",
                permanent=True,
                protocol="HTTPS",
                query="#{query}"
            ),
        )
        alb.add_listener(
            id=CdkConfig.config['alb_resources']['listeners']['id_443'],
            port=443,
            open=False,
            default_target_groups=[targetgroup],
            certificate_arns=["arn:aws:acm:us-east-1:748208346432:\
                certificate/9292c84a-9da3-4c28-afce-fb258e046082"]
        )
        test_alb_assert = self.mock_application_load_balancer.return_value
        self.assertEqual(test_alb_act, test_alb_assert)
