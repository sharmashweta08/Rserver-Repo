# CFN lint is used to analyse cloud formation code for errors, stylistic errors and bugs

set -e

pip install cfn-lint

cfn-lint --template infra/cdk.out/*.template.json --ignore-checks W2001,W3005,W3010