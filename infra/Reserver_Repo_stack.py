'''Rserver repository stack'''
from aws_cdk import core
from aws_cdk.aws_route53 import HostedZone
from services.iam_construct import IamService
from services.network_construct import NetworkService
from services.iam_construct import IamService
from services.ec2_construct import EC2Service
from services.alb_construct import AlbService
from services.ssl_construct import SSLService
from services.hosted_zone_construct import HostedZoneService
from config import CdkConfig

class RserverRepoStack(core.Stack):
    """Inegi Repo Stack Class"""
    def __init__(self, scope:core.Construct, construct_id: str, **kwargs):      #pylint: disable=R0914
        """Main function"""
        stack = self
        super().__init__(scope, construct_id, **kwargs)
        if construct_id == CdkConfig.config['hosted_zone_stack_name'] and CdkConfig.hosted_zone_deploy == 'true':
            HostedZoneService.create_hosted_zone(stack)
        if construct_id == CdkConfig.config['primary_rserver_stack_name'] and CdkConfig.primary_rserver_deploy == 'true' and CdkConfig.hosted_zone_deploy == 'false':
            iamrole = IamService.create_iam_role(stack)
            vpc = NetworkService.get_vpc(stack)
            private_subnet = NetworkService.private_subnet_selection(stack)
            public_subnet = NetworkService.public_subnet_selection(stack)
            alb_security_group = NetworkService.create_alb_security_group(stack, vpc)
            ec2_securitygroup = NetworkService.create_ec2_security_group(stack, vpc, alb_security_group)
            ec2server = EC2Service.create_ec2_service(stack, vpc, private_subnet, ec2_securitygroup, iamrole)
            rserver_hosted_zone = HostedZoneService.get_hosted_zone(stack)
            certificate = SSLService.create_ssl(stack, rserver_hosted_zone)
            alb = AlbService.create_alb(stack, vpc, ec2server, public_subnet, alb_security_group,\
                 certificate.certificate_arn)
            HostedZoneService.create_a_record(stack, alb, rserver_hosted_zone)

        
