'''Construct File of EC2'''
from aws_cdk import aws_ec2

from config import CdkConfig

class EC2Service():
    """EC2 Service Class"""
    @staticmethod
    def create_ec2_service(stack, vpc, private_subnet, securitygroup, iamrole):
        """Creation of EC2 service"""
        ec2server = aws_ec2.Instance(
            scope=stack,
            id=CdkConfig.config['ec2_resources']['id'],
            instance_name=CdkConfig.config['ec2_resources']['instance_name'],
            instance_type=aws_ec2.InstanceType(
                instance_type_identifier=CdkConfig.config['ec2_resources']['instance_type_identifier']
            ),
            machine_image=aws_ec2.MachineImage.generic_linux(
                {CdkConfig.config['region']:CdkConfig.config['ec2_resources']['machine_image']}
            ),
            vpc=vpc,
            vpc_subnets=private_subnet,
            security_group=securitygroup,
            role=iamrole
        )
        ec2server.user_data.add_commands(
            "yum update -y",
            "amazon-linux-extras install R4 -y",
            "wget https://download2.rstudio.org/rstudio-server-rhel-1.0.153-x86_64.rpm",
            "yum install -y --nogpgcheck rstudio-server-rhel-1.0.153-x86_64.rpm",
            "rm rstudio-server-rhel-1.0.153-x86_64.rpm",
            "R -e 'install.packages('shiny', repos='http://cran.rstudio.com/')'",
            "wget https://download3.rstudio.org/centos5.9/x86_64/shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "yum install -y --nogpgcheck shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "rm -f shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "yum install -y git"
        )
        return ec2server