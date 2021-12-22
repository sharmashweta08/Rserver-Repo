'''Construct File for Hosted Zone'''
from aws_cdk import aws_route53
from aws_cdk import aws_route53_targets

from config import CdkConfig

class HostedZoneService():
    @staticmethod
    def create_hosted_zone(stack):
        rserver_hosted_zone = aws_route53.HostedZone(
            scope=stack,
            id=CdkConfig.config['hosted_zone_resources']['rserver_hosted_zone']['id'],
            zone_name=CdkConfig.config['hosted_zone_resources']['rserver_hosted_zone']['zone_name']
        )
        return rserver_hosted_zone

    @staticmethod
    def get_hosted_zone(stack):
        get_the_zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            scope=stack,
            id=CdkConfig.config['hosted_zone_resources']['get_hosted_zone']['id'],
            hosted_zone_id=CdkConfig.config['hosted_zone_resources']['get_hosted_zone']['hosted_zone_id'],
            zone_name=CdkConfig.config['hosted_zone_resources']['rserver_hosted_zone']['zone_name']
        )
        return get_the_zone

    @staticmethod
    def create_a_record(stack, alb, rserver_hosted_zone):
        a_record = aws_route53.ARecord(
            scope=stack,
            id=CdkConfig.config['hosted_zone_resources']['a_record']['id'],
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.LoadBalancerTarget(alb)
            ),
            zone=rserver_hosted_zone
        )
        return a_record
    