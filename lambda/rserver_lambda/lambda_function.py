import json
import boto3
import time

ssm_client = boto3.client('ssm')
ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    instance_id = []
    reservation = ec2_client.describe_instances(
        Filters = [{
            'Name':'tag:Name',
            'Values':['Rserver',]
        },],DryRun=False).get('Reservations', [])
    instances = sum([[i for i in r['Instances']]for r in reservation], [])
    for instance in instances:
        if instance["State"]["Name"]=="running":
            instance_id.append(instance['InstanceId'])
    for id in instance_id:
        response = ssm_client.send_command(
            InstanceIds=[
                id,
            ],
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'adduser ankit',
                    'echo ankit:Qwerty@123 | chpasswd',
                    "su - ankit -c 'git config --global credential.helper \"!aws codecommit credential-helper $@\"'",
                    "su - ankit -c 'git config --global credential.UseHttpPath true'",
                    "su - ankit -c 'git config --global user.email \"ss.meetu1994@gmail.com\"'",
                    "su - shweta -c 'git config --global user.name \"Shweta\"'",
                    'echo "shweta ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/rserver-users',
                    "chmod -R 440 /etc/sudoers.d/rserver-users",
                    "chmod -R 757 /usr/lib64/R/library/",
                    "chmod -R 757 /usr/share/doc/R-4.0.2/html/"
                ]
            },
        )
        command_id = response['Command']['CommandId']
        time.sleep(6)
        output = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=id
        )
        print(output)
    