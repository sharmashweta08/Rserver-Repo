'''config.py'''
import json
import os

class CdkConfig():   # pylint: disable=too-few-public-methods
    """CDK confif class"""
    with open('appsettings.json') as file:
        config = json.load(file)
        primary_rserver_deploy = os.getenv('PRIMARY_RSERVER_DEPLOY', 'true')
        hosted_zone_deploy = os.getenv('HOSTED_ZONE_DEPLOY', 'false')
