from aws_cdk import (
    Stack,
    aws_apigatewayv2 as apigateway,
    aws_apigatewayv2_integrations as integrations,
)
from constructs import Construct

class httpApi(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        eb_app_url = 'http://romanneudakh-bff-api-task-10.eu-west-1.elasticbeanstalk.com/'
        cors_preflight = apigateway.CorsPreflightOptions(
            allow_origins=["*"], 
            allow_methods=[apigateway.CorsHttpMethod.ANY], 
            allow_headers=["*"],
        )
        api = apigateway.HttpApi(
            self, "HttpApi",
            api_name="ebProxyApi",
            description="This API proxies to eb application",
            cors_preflight=cors_preflight 
        )
        integration_cart = integrations.HttpUrlIntegration(
            'ebIntegration',
            url=f"{eb_app_url}cart"
        )
        api.add_routes(
            path="/cart",
            methods=[apigateway.HttpMethod.ANY], 
            integration=integration_cart
        )
        integration_product = integrations.HttpUrlIntegration(
            'ebIntegration',
            url=f"{eb_app_url}product"
        )
        api.add_routes(
            path="/product",
            methods=[apigateway.HttpMethod.ANY], 
            integration=integration_product
        )
        integration_root = integrations.HttpUrlIntegration(
            'ebIntegration',
            url=eb_app_url
        )
        api.add_routes(
            path="/{proxy+}",
            methods=[apigateway.HttpMethod.ANY],
            integration=integration_root
        )
