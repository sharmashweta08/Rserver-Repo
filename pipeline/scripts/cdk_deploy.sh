set -e

# for deploying CDK

cd $1
cd infra
sudo npm install -g aws-cdk@$4
sudo npm update -g aws-cdk

export AWS_DEFAULT_REGION=$3

cdk deploy --require-approval never