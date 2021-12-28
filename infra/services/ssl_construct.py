'''Construct File For SSL'''
from aws_cdk import core
from aws_cdk import aws_certificatemanager
from config import CdkConfig

class SSLService():
    """SSL Service Class"""
    @staticmethod
    def create_ssl(stack,rserver_hosted_zone):
        """Creating SSL - Function"""
        certificate = aws_certificatemanager.Certificate(
            scope=stack,
            id=CdkConfig.config['ssl_resources']['id'],
            domain_name=CdkConfig.config['ssl_resources']['domain_name'],
            validation=aws_certificatemanager.CertificateValidation.from_dns(
                hosted_zone=rserver_hosted_zone
            )
        )
        core.Tags.of(certificate).add(
            key=CdkConfig.config['ssl_resources']['tag_key'],
            value=CdkConfig.config['ssl_resources']['tag_value']
        )
        return certificate
