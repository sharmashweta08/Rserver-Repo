'''Construct File for Network'''
from aws_cdk import aws_ec2
from config import CdkConfig

class NetworkService():
    """Network Service Class"""
    @staticmethod
    def get_vpc(stack):
        """Getting the value of VPC"""
        vpc_resource = aws_ec2.Vpc.from_vpc_attributes(
            scope=stack,
            id=CdkConfig.config['network_resources']['vpc_resource']['id'],
            availability_zones=[
                CdkConfig.config['network_resources']['vpc_resource']['availability_zones']
            ],
            vpc_id=CdkConfig.config['network_resources']['vpc_resource']['vpc_id']
        )
        return vpc_resource

    @staticmethod
    def get_private_subnet_01(stack):
        """Getting the value of Subnet 1"""
        private_subnet_resource_01 = aws_ec2.Subnet.from_subnet_attributes(
            scope=stack,
            id=CdkConfig.config['network_resources']['private_subnet']['subnet_resource_01']['id'],
            availability_zone=CdkConfig.config['network_resources']\
                ['private_subnet']['subnet_resource_01']['availability_zone'],
            subnet_id=CdkConfig.config['network_resources']['private_subnet']['subnet_resource_01']['subnet_id']
        )
        return private_subnet_resource_01

    @staticmethod
    def get_private_subnet_02(stack):
        """Getting the value of Subnet 2"""
        private_subnet_resource_02 = aws_ec2.Subnet.from_subnet_attributes(
            scope=stack,
            id=CdkConfig.config['network_resources']['private_subnet']['subnet_resource_02']['id'],
            availability_zone=CdkConfig.config['network_resources']\
                ['private_subnet']['subnet_resource_02']['availability_zone'],
            subnet_id=CdkConfig.config['network_resources']['private_subnet']['subnet_resource_02']['subnet_id']
        )
        return private_subnet_resource_02

    @staticmethod
    def private_subnet_selection(stack):
        """Selection of Subnets"""
        private_subnets = aws_ec2.SubnetSelection(
            subnets=[NetworkService.get_private_subnet_01(stack), NetworkService.get_private_subnet_02(stack)],
        )
        return private_subnets

    @staticmethod
    def get_public_subnet_01(stack):
        """Getting the value of Subnet 1"""
        public_subnet_resource_01 = aws_ec2.Subnet.from_subnet_attributes(
            scope=stack,
            id=CdkConfig.config['network_resources']['public_subnet']['subnet_resource_01']['id'],
            availability_zone=CdkConfig.config['network_resources']\
                ['public_subnet']['subnet_resource_01']['availability_zone'],
            subnet_id=CdkConfig.config['network_resources']['public_subnet']['subnet_resource_01']['subnet_id']
        )
        return public_subnet_resource_01

    @staticmethod
    def get_public_subnet_02(stack):
        """Getting the value of Subnet 2"""
        public_subnet_resource_02 = aws_ec2.Subnet.from_subnet_attributes(
            scope=stack,
            id=CdkConfig.config['network_resources']['public_subnet']['subnet_resource_02']['id'],
            availability_zone=CdkConfig.config['network_resources']\
                ['public_subnet']['subnet_resource_02']['availability_zone'],
            subnet_id=CdkConfig.config['network_resources']['public_subnet']['subnet_resource_02']['subnet_id']
        )
        return public_subnet_resource_02

    @staticmethod
    def public_subnet_selection(stack):
        """Selection of Subnets"""
        public_subnets = aws_ec2.SubnetSelection(
            subnets=[NetworkService.get_public_subnet_01(stack), NetworkService.get_public_subnet_02(stack)],
        )
        return public_subnets

    def create_alb_security_group(stack, vpc):
        """Creation of Security Group"""
        alb_security_group = aws_ec2.SecurityGroup(
            scope=stack,
            id=CdkConfig.config['network_resources']['alb_security_group']['id'],
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name=CdkConfig.config['network_resources']\
                ['alb_security_group']['security_group_name']
        )
        alb_security_group.add_ingress_rule(
            aws_ec2.Peer.any_ipv4(),
            aws_ec2.Port.tcp(80),
            description=CdkConfig.config['network_resources']['alb_security_group']['description_80']
        )
        alb_security_group.add_ingress_rule(
            aws_ec2.Peer.any_ipv4(),
            aws_ec2.Port.tcp(443),
            description=CdkConfig.config['network_resources']['alb_security_group']['description_443']
        )
        return alb_security_group

    @staticmethod
    def create_ec2_security_group(stack, vpc, alb_securitygroup):
        """Creation of Security Group"""
        ec2_security_group = aws_ec2.SecurityGroup(
            scope=stack,
            id=CdkConfig.config['network_resources']['ec2_security_group']['id'],
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name=CdkConfig.config['network_resources']\
                ['ec2_security_group']['security_group_name']
        )
        ec2_security_group.add_ingress_rule(
            alb_securitygroup,
            aws_ec2.Port.tcp(8787),
            description="Allow ALB to EC2"
        )
        return ec2_security_group
    
    