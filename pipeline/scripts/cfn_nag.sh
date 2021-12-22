# CFN-NAG is a popular open-source tool developed by Stelligent and provided to the open-sorce community to help pin-point security problems
# early on in an AWS cloud formation template.

sudo gem install cfn-nag
sudo cfn_nag_scan --input-path infra/cdk.out/*.template.json