from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as lambda_,
)
from constructs import Construct
import os
from dotenv import load_dotenv
class DeploymentStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        load_dotenv()
        basic_authorizer = lambda_.Function(
            self, 'BasicAuthorizer',
            function_name='BasicAuthorizer',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('authorization_service_aws_shop/lambda_handlers/'),
            handler='authorization_handler.authorizationHandler',
            environment={
                os.getenv('GITHUB_ACCOUNT_LOGIN'): os.getenv('TEST_PASSWORD'),
            }
        )
        CfnOutput(
            self, 
            'BasicAuthorizerName', 
            value=basic_authorizer.function_name, 
            export_name='BasicAuthorizerName'
        )
