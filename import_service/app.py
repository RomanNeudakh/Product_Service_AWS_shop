import aws_cdk as cdk
from import_service_aws_shop.lambda_functions.deployment_stack import DeploymentStack

app = cdk.App()
DeploymentStack(app, "ImportServiceAwsShopStackCrosscheck")
app.synth()
