'''aap.py'''
from aws_cdk import core
from Reserver_Repo_stack import RserverRepoStack
from config import CdkConfig

resource = core.App()
region = core.Environment(account="748208346432", region='us-east-1')
if CdkConfig.primary_rserver_deploy == 'true':
    RserverRepoStack(
        scope = resource,
        env = region,
        construct_id = CdkConfig.config['primary_rserver_stack_name'],
        description = CdkConfig.config['primary_rserver_stack_description'],
        tags = CdkConfig.config['tags']
    )
if CdkConfig.hosted_zone_deploy == 'true':
    RserverRepoStack(
        scope = resource,
        env = region,
        construct_id = CdkConfig.config['hosted_zone_stack_name'],
        description = CdkConfig.config['hosted_zone_stack_description'],
        tags = CdkConfig.config['tags']
    )
resource.synth()
