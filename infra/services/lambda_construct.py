'''Construct File of Lambda'''
from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_logs
from config import CdkConfig

class LambdaService():
    """Lambda service class"""
    @staticmethod
    def create_rserver_lambda(stack, iam_role):
        """Creation of Inegi raw lambda service"""
        lambda_service = aws_lambda.Function(
            scope=stack,
            id=CdkConfig.config['lambda_resources']['id'],
            code=aws_lambda.Code.from_asset(
                path=CdkConfig.config['lambda_resources']['path']
            ),
            handler=CdkConfig.config['lambda_resources']['handler'],
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            function_name=CdkConfig.config['lambda_resources']['function_name'],
            role=iam_role,
            timeout=core.Duration.minutes(CdkConfig.config['lambda_resources']['duration']),
            memory_size=CdkConfig.config['lambda_resources']['memory_size'],
            log_retention=aws_logs.RetentionDays.ONE_MONTH,
            environment={
                "instance_name" : CdkConfig.config['ec2_resources']['instance_name'],
                "env" : CdkConfig.config['env']
            }
        )
        return lambda_service
