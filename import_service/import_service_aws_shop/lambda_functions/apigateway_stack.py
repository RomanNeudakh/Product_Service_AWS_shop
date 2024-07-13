from aws_cdk import (
    aws_apigateway as apigateway,
    Stack,
    Fn,
    aws_lambda as lambda_,
)
from constructs import Construct

class ApiGatewayStack(Stack):
    def __init__(self, scope: Construct, id: str, import_lambda, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        api = apigateway.RestApi(
            self, 
            "ImportServiceApi",
            rest_api_name="Import Service",
            description="This service imports csv products file.",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["*"]
            )
        )
        basic_authorizer_name = Fn.import_value('BasicAuthorizerName')
        authorizer = apigateway.TokenAuthorizer(
            self, 'BasicAuthorizer',
            handler=lambda_.Function.from_function_name(self, 'ImportedAuthorizer', basic_authorizer_name)
        )
        import_integration = apigateway.LambdaIntegration(import_lambda)
        import_resource = api.root.add_resource("import")
        import_resource.add_method(
            "GET", 
            import_integration, 
            authorization_type=apigateway.AuthorizationType.CUSTOM, 
            authorizer=authorizer
        )