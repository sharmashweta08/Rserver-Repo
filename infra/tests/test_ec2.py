'''Unit Test for ALB Service'''
import unittest
from unittest.mock import patch, Mock
from services.ec2_construct import EC2Service
from config import CdkConfig

class TestEC2Service(unittest.TestCase):      #pylint: disable=too-many-instance-attributes
    """Test EC2 Service class"""
    def setUp(self):
        """Setup Function"""
        self.addCleanup(patch.stopall)
        self.mock_stack=Mock()
        self.mock_vpc=Mock()
        self.mock_private_subnet=Mock()
        self.mock_security_group=Mock()
        self.mock_iamrole=Mock()
        self.mock_ec2server=Mock()
        self.mock_ec2_instance=patch("aws_cdk.aws_ec2.Instance", spec=True).start()
        self.mock_ec2_instance_type=patch("aws_cdk.aws_ec2.InstanceType", spec=True).start()
        self.mock_ec2_machine_image=patch("aws_cdk.aws_ec2.MachineImage", spec=True).start()

    def test_create_security_group_expected_parameters(self):
        """Create SG Function"""
        #Act
        test_ec2_act = EC2Service.create_ec2_service(self.mock_stack, self.mock_vpc, \
            self.mock_private_subnet, self.mock_security_group, self.mock_iamrole)
        #Assert
        self.mock_ec2_instance.assert_called_with(
            scope=self.mock_stack,
            id=CdkConfig.config['ec2_resources']['id'],
            instance_name=CdkConfig.config['ec2_resources']['instance_name'],
            instance_type=self.mock_ec2_instance_type(
                instance_type_identifier=CdkConfig.config['ec2_resources']\
                    ['instance_type_identifier']
            ),
            machine_image=self.mock_ec2_machine_image.generic_linux(
                {CdkConfig.config['region']:CdkConfig.config['ec2_resources']['machine_image']}
            ),
            vpc=self.mock_vpc,
            vpc_subnets=self.mock_private_subnet,
            security_group=self.mock_security_group,
            role=self.mock_iamrole
        )
        self.mock_ec2server.user_data.add_commands(
            "yum update -y",
            "amazon-linux-extras install R4 -y",
            "wget https://download2.rstudio.org/rstudio-server-rhel-1.0.153-x86_64.rpm",
            "yum install -y --nogpgcheck rstudio-server-rhel-1.0.153-x86_64.rpm",
            "rm rstudio-server-rhel-1.0.153-x86_64.rpm",
            "R -e 'install.packages('shiny', repos='http://cran.rstudio.com/')'",
            "wget \
            https://download3.rstudio.org/centos5.9/x86_64/shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "yum install -y --nogpgcheck shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "rm -f shiny-server-1.5.4.869-rh5-x86_64.rpm",
            "yum install -y git"
        )
        test_ec2_assert = self.mock_ec2_instance.return_value
        self.assertEqual(test_ec2_act, test_ec2_assert)
