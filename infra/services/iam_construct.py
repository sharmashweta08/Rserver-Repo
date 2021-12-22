'''Construct of IAM'''
from aws_cdk import aws_iam
from config import CdkConfig

class IamService():
    """IAM service class"""
    @staticmethod        #will be called by using class name.function name
    def create_iam_role(stack):
        """Creation of IAM Role"""
        iam_role = aws_iam.Role(
            scope = stack,
            id=CdkConfig.config['iam_resources']['id'],
            role_name=CdkConfig.config['iam_resources']['role_name'],
            assumed_by=aws_iam.CompositePrincipal(
                aws_iam.ServicePrincipal('lambda.amazonaws.com'),
                aws_iam.ServicePrincipal('s3.amazonaws.com'),
                aws_iam.ServicePrincipal('cloudwatch.amazonaws.com'),
                aws_iam.ServicePrincipal('glue.amazonaws.com')
            )
        )
        iam_role.add_to_policy(IamService.ec2_policy())
        iam_role.add_to_policy(IamService.ec2_msg_policy())
        iam_role.add_to_policy(IamService.ssm_policy())
        iam_role.add_to_policy(IamService.ssm_message_policy())
        iam_role.add_to_policy(IamService.cloudwatch_policy())
        iam_role.add_to_policy(IamService.logs_policy())
        iam_role.add_to_policy(IamService.lambda_policy())

        return iam_role

    @staticmethod
    def ec2_policy():                       # bcoz we have to use security groups
        """Policy of EC2"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions("ec2:DescribeNetworkInterfaces")
        policy_statement.add_actions("ec2:CreateNetwork")
        policy_statement.add_actions("ec2:CreateNetworkInterface")
        policy_statement.add_actions("ec2:DeleteNetworkInterface")
        policy_statement.add_actions("ec2:DescribeInstances")
        policy_statement.add_actions("ec2:AttachNetworkInterface")
        policy_statement.add_actions("ec2:DescribeImages")
        policy_statement.add_actions("ec2:DescribeTags")
        policy_statement.add_actions("ec2:DescribeSnapshots")
        policy_statement.add_actions("ec2:DescribeInstanceTypes")
        policy_statement.add_actions("ec2:DescribeKeyPairs")
        policy_statement.add_actions("ec2:DescribeVpcs")
        policy_statement.add_actions("ec2:DescribeSubnets")
        policy_statement.add_actions("ec2:DescribeSecurityGroups")
        policy_statement.add_actions("ec2:CreateSecurityGroup")
        policy_statement.add_actions("ec2:AuthorizeSecurityGroupIngress")
        policy_statement.add_actions("ec2:CreateKeyPair")
        policy_statement.add_actions("ec2:RunInstances")
        policy_statement.add_actions("ec2:DescribeInstanceStatus")
        policy_statement.add_actions("ec2:CreateImage")
        policy_statement.add_actions("ec2:CreateTags")
        policy_statement.add_actions("ec2:CopyImage")
        policy_statement.add_actions("ec2:DeRegisterImage")
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def ec2_msg_policy():
        """Policy of EC2 Message"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions("ec2messages:AcknowledgeMessage")
        policy_statement.add_actions("ec2messages:DeleteMessage")
        policy_statement.add_actions("ec2messages:FailMessage")
        policy_statement.add_actions("ec2messages:GetEndpoint")
        policy_statement.add_actions("ec2messages:GetMessages")
        policy_statement.add_actions("ec2messages:SendReply")
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def ssm_message_policy():
        """Policy of SSM"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions("ssmmessages:CreateControlChannel")
        policy_statement.add_actions("ssmmessages:CreateDataChannel")
        policy_statement.add_actions("ssmmessages:OpenControlChannel")
        policy_statement.add_actions("ssmmessages:OpenDataChannel")
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def ssm_policy():
        """Policy of SSM"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions("ssm:DescribeAssociation")
        policy_statement.add_actions("ssm:GetDeployablePatchSnapshotForInstance")
        policy_statement.add_actions("ssm:GetDocument")
        policy_statement.add_actions("ssm:DescribeDocument")
        policy_statement.add_actions("ssm:GetManifest")
        policy_statement.add_actions("ssm:GetParameters")
        policy_statement.add_actions("ssm:ListAssociation")
        policy_statement.add_actions("ssm:ListInstanceAssociations")
        policy_statement.add_actions("ssm:PutInventory")
        policy_statement.add_actions("ssm:PutComplianceItems")
        policy_statement.add_actions("ssm:PutConfigurePackageResult")
        policy_statement.add_actions("ssm:UpdateAssociationStatus")
        policy_statement.add_actions("ssm:UpdateInstanceAssociationStatus")
        policy_statement.add_actions("ssm:UpdateInstanceInformation")
        policy_statement.add_actions("ssm:SendCommand")
        policy_statement.add_actions("ssm:ListCommands")
        policy_statement.add_actions("ssm:ListCommandInvocations")
        policy_statement.add_actions("ssm:GetCommandInvocation")
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def cloudwatch_policy():
        """Policy of Cloudwatch"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions('cloudwatch:DescribeAlarms')
        policy_statement.add_actions('cloudwatch:GetMetricData')
        policy_statement.add_actions('cloudwatch:GetMetricStatistics')
        policy_statement.add_actions('cloudwatch:ListMetrics')
        policy_statement.add_actions('cloudwatch:PutMetricAlarm')
        policy_statement.add_actions('cloudwatch:PutMetricData')
        policy_statement.add_all_resources()

        return policy_statement


    @staticmethod
    def logs_policy():
        """Policy of Logs"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions('logs:CreateLogGroup')
        policy_statement.add_actions('logs:CreateLogStream')
        policy_statement.add_actions('logs:DescribeLogGroups')
        policy_statement.add_actions('logs:DescribeLogStream')
        policy_statement.add_actions('logs:FilterLogEvents')
        policy_statement.add_actions('logs:GetLogEvents')
        policy_statement.add_actions('logs:DeleteLogGroup')
        policy_statement.add_actions('logs:PutLogEvents')
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def codecommit_policy():
        """Policy of Code Commit"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions('codecommit:GetRepository')
        policy_statement.add_actions('codecommit:CreateRepository')
        policy_statement.add_actions('codecommit:ListRepositories')
        policy_statement.add_actions('codecommit:UpdateRepositoryDescription')
        policy_statement.add_actions('codecommit:UpdateRepositoryName')
        policy_statement.add_actions('codecommit:GitPull')
        policy_statement.add_actions('codecommit:GitPush')
        policy_statement.add_actions('codecommit:CreateBranch')
        policy_statement.add_actions('codecommit:GetBranch')
        policy_statement.add_actions('codecommit:ListBranches')
        policy_statement.add_actions('codecommit:MergeBranchesByFastForward')
        policy_statement.add_actions('codecommit:MergeBranchesBySquash')
        policy_statement.add_actions('codecommit:MergeBranchesByThreeWay')
        policy_statement.add_actions('codecommit:UpdateDefaultBranch')
        policy_statement.add_actions('codecommit:BatchDescribeMergeConflicts')
        policy_statement.add_actions('codecommit:GetMergeCommit')
        policy_statement.add_actions('codecommit:GetMergeOptions')
        policy_statement.add_actions('codecommit:BatchGetPullRequests')
        policy_statement.add_actions('codecommit:CreatePullRequest')
        policy_statement.add_actions('codecommit:CreatePullRequestApprovalRule')
        policy_statement.add_actions('codecommit:GetCommentsForPullRequest')
        policy_statement.add_actions('codecommit:GetCommitsFromMergeBase')
        policy_statement.add_actions('codecommit:GetMergeConflicts')
        policy_statement.add_actions('codecommit:GetPullRequest')
        policy_statement.add_actions('codecommit:GetPullRequestApprovalStates')
        policy_statement.add_actions('codecommit:GetPullRequestOverrideState')
        policy_statement.add_actions('codecommit:ListPullRequests')
        policy_statement.add_actions('codecommit:MergePullRequestByFastForward')
        policy_statement.add_actions('codecommit:MergePullRequestBySquash')
        policy_statement.add_actions('codecommit:MergePullRequestByThreeWay')
        policy_statement.add_actions('codecommit:PostCommentForPullRequest')
        policy_statement.add_actions('codecommit:UpdatePullRequestDescription')
        policy_statement.add_actions('codecommit:UpdatePullRequestStatus')
        policy_statement.add_actions('codecommit:UpdatePullRequestTitle')
        policy_statement.add_actions('codecommit:GetBlob')
        policy_statement.add_actions('codecommit:GetFile')
        policy_statement.add_actions('codecommit:GetFolder')
        policy_statement.add_actions('codecommit:PutFile')
        policy_statement.add_actions('codecommit:GetComment')
        policy_statement.add_actions('codecommit:UpdateComment')
        policy_statement.add_actions('codecommit:BatchGetCommits')
        policy_statement.add_actions('codecommit:CreateCommit')
        policy_statement.add_actions('codecommit:GetCommit')
        policy_statement.add_actions('codecommit:GetCommitHistory')
        policy_statement.add_actions('codecommit:GetDifferences')
        policy_statement.add_actions('codecommit:GetObjectIdentifier')
        policy_statement.add_actions('codecommit:GetReferences')
        policy_statement.add_actions('codecommit:GetTree')
        policy_statement.add_actions('codecommit:BatchGetRepositories')
        policy_statement.add_all_resources()

        return policy_statement

    @staticmethod
    def lambda_policy():
        """Policy of Lambda"""
        policy_statement = aws_iam.PolicyStatement()
        policy_statement.effect = aws_iam.Effect.ALLOW
        policy_statement.add_actions('lambda:InvokeFunction')
        policy_statement.add_actions('lambda:UpdateFunctionConfiguration')
        policy_statement.add_resources("arn:aws:lambda:"+CdkConfig.config['region']+\
            ":"+CdkConfig.config['account_id']+":function:"+\
                CdkConfig.config['lambda_resources']['function_name'])

        return policy_statement