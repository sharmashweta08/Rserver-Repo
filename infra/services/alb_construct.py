'''Construct File of Application Load Balancer'''
from aws_cdk import aws_ec2
from aws_cdk import aws_elasticloadbalancingv2
from aws_cdk import aws_elasticloadbalancingv2_targets
from config import CdkConfig

class AlbService():
    @staticmethod
    def create_alb(stack, vpc, ec2server, public_subnet, alb_security_group, certificate_arn):
        targetgroup = aws_elasticloadbalancingv2.ApplicationTargetGroup(
            scope=stack,
            id=CdkConfig.config['alb_resources']['targetgroup']['id'],
            target_type=aws_elasticloadbalancingv2.TargetType.INSTANCE,
            target_group_name=CdkConfig.config['alb_resources']['targetgroup']['target_group_name'],
            vpc=vpc,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            port=CdkConfig.config['alb_resources']['targetgroup']['port'],
            protocol_version=aws_elasticloadbalancingv2.ApplicationProtocolVersion.HTTP1,
            health_check={
                "enabled" : True,
                "port" : "8787",
                "path" : "/auth-sign-in"
            }
        )
        targetgroup.add_target(
            aws_elasticloadbalancingv2_targets.InstanceIdTarget(ec2server.instance_id)
        )
        alb = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            scope=stack,
            id=CdkConfig.config['alb_resources']['alb']['id'],
            load_balancer_name=CdkConfig.config['alb_resources']['alb']['load_balancer_name'],
            internet_facing=True,
            vpc=vpc,
            vpc_subnets=public_subnet,
            security_group=alb_security_group
        )
        alb.add_listener(
            id=CdkConfig.config['alb_resources']['listeners']['id_80'],
            port=80,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTP,
            open=False,
            default_action=aws_elasticloadbalancingv2.ListenerAction.redirect(
                host="#{host}",
                path="/#{path}",
                port="443",
                permanent=True,
                protocol="HTTPS",
                query="#{query}"
            )
        )
        alb.add_listener(
            id=CdkConfig.config['alb_resources']['listeners']['id_443'],
            port=443,
            protocol=aws_elasticloadbalancingv2.ApplicationProtocol.HTTPS,
            open=False,
            default_target_groups=[targetgroup],
            certificate_arns=[certificate_arn]
        )
        return alb
        